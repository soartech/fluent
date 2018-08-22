import json
from datetime import datetime
import cass_client.api.cass_single_object_api
from typing import List, Dict, Optional

# http://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Framework/59e884bb-510b-4f36-8443-8c3842336e28


def unique(list_):
    return list(set(list_))


# Needed for using json.dumps with abnormal types, like datetime
# This is kind of experimental, and might be total garbage
def safe_vars(obj: object, depth=0):
    if type(obj) is cass_client.Competency and depth > 0:
        return obj.id

    try:
        out_dict = dict(vars(obj))
    except TypeError:
        return obj

    for name, value in out_dict.items():
        if type(value) is datetime:
            out_dict[name] = str(value)
        elif type(value) is cass_client.Competency:
            out_dict[name] = safe_vars(value, depth+1)
        elif type(value) is dict:
            out_dict[name] = dict([(child_name, safe_vars(child_value, depth+1)) for child_name, child_value in value.items()])
        else:
            out_dict[name] = value
    return out_dict


class CassGraph:

    def __init__(self, framework_id: str, cass_single_object_api: cass_client.CASSSingleObjectApi = cass_client.CASSSingleObjectApi()):
        self._cass_object_api = cass_single_object_api
        self.competency_objs = {}
        self.relation_objs = {}
        self.first_top_level_competency = None
        self.top_level_competencies = {}

        self._pull_all_data_from_cass(framework_id)

        print("Calculating node parents and children..")
        self._calculate_node_levels()

        print("Calculating node order...")
        self.first_top_level_competency = self._calculate_node_order(self.top_level_competencies.values())

        output_json = json.loads('{ "competencies": [], "relations": []}')

        output_json['competencies'] = [safe_vars(obj) for obj in self.competency_objs.values()]
        output_json['relations'] = [safe_vars(obj) for obj in self.relation_objs.values()]

        # file = open('relations.json', 'w')
        # file.write(json.dumps(output_json, indent=4))
        # file.close()

        del(self._cass_object_api)

    def __str__(self):
        output = ""
        node = self.first_top_level_competency
        while node is not None:
            output += self.competency_to_str_with_children(node)
            node = getattr(node, "next_neighbor", None)
        return output

    def _pull_all_data_from_cass(self, framework_id: str):
        framework = self._cass_object_api.get_framework(framework_id)

        competency_urls = framework.competency
        relation_urls = framework.relation

        # This is the step that takes a while due to many http requests
        print("Getting competencies...")
        for url in competency_urls:
            self.competency_objs[url] = self._cass_object_api.get_competency(self.get_id_from_url(url))
            # Yay for python allowing dynamic adding of attributes. No wrapper class needed
            self.competency_objs[url].id = url
            self.competency_objs[url].first_child = None
            self.competency_objs[url].children = {}
            self.competency_objs[url].parent = None
            self.competency_objs[url].level = -1
            self.competency_objs[url].next_neighbor = None
            self.competency_objs[url].prev_neighbor = None
            self.competency_objs[url].requires = []
        print("Getting relations...")
        for url in relation_urls:
            self.relation_objs[url] = self._cass_object_api.get_relation(self.get_id_from_url(url))
            if self.relation_objs[url].source == self.relation_objs[url].target:
                del self.relation_objs[url]

        print("Adding requires relations to competency objects")
        for competency in self.competency_objs.values():
            requires_relations = self.get_relations(relation_type="requires", source=competency.id)
            competency.requires = [self.get_obj_by_id(relation.target) for relation in requires_relations]


    def _propagate_nodes_down(self, id_list):
        next_id_list = []
        for url in id_list:
            obj = self.competency_objs[url]

            children_list = [obj2.source for obj2 in self.get_relations(relation_type="narrows", target=obj.id)]
            parents_list = [obj2.target for obj2 in self.get_relations(relation_type="narrows", source=obj.id)]
            for child_url in children_list:
                if child_url not in obj.children:
                    obj.children[child_url] = self.competency_objs.get(child_url)

            if parents_list:
                obj.parent = self.competency_objs.get(parents_list[0])  # We are expecting there to be only one parent

            obj.level += 1

            next_id_list += children_list

        next_id_list = unique(next_id_list)
        if next_id_list:
            self._propagate_nodes_down(next_id_list)

    def _calculate_node_levels(self):
        source_list = unique([item.source for item in self.get_relations(relation_type="narrows")])
        comp_id_list = [item.id for item in self.competency_objs.values()]

        top_level_urls = [item for item in comp_id_list if item not in source_list]

        for url in top_level_urls:
            self.top_level_competencies[url] = self.competency_objs[url]

        self._propagate_nodes_down(self.top_level_competencies)

    # Returns a first child in order, to be used to establish the first_child field of all competencies
    def _calculate_node_order(self, competencies_list=None):

        # We need to be able to remove from this list without affecting the data outside of the function
        # Thus we copy the list
        unprocessed_nodes = list(competencies_list)

        first_child = None

        # The first ordered node can be determined by the fact that it shouldn't require anything
        for node in unprocessed_nodes:
            if not self.get_relations(relation_type="requires", source=node.id):
                first_child = node
                break

        for node in unprocessed_nodes:  # type: cass_client.Competency
            node_children = self.get_children(node)
            if node_children:
                # Do the recursive step first. So we sort from the deepest layer upward
                # The recursion stops when we hit the deepest later and a node has no children
                node.first_child = self._calculate_node_order(node_children)

        prev_child = first_child
        # Acknowledge that we've seen the first child already
        self._remove_comp_from_list(unprocessed_nodes, first_child)  # Error prevention method

        # Then deal with the rest
        while unprocessed_nodes:
            for unprocessed_node in unprocessed_nodes:
                # If the node doesn't point to any other unprocessed node in the list
                # Then it only points at nodes we've processed already, and is thus the next one in the order
                if not self.get_relations(relation_type="requires",
                                          source=unprocessed_node.id,
                                          target=[c.id for c in unprocessed_nodes]
                                          ):
                    # Establish neighbors
                    prev_child.next_neighbor = unprocessed_node
                    unprocessed_node.prev_neighbor = prev_child

                    # Prepare for next iteration of loop
                    self._remove_comp_from_list(unprocessed_nodes, unprocessed_node)  # Error prevention method
                    prev_child = unprocessed_node
                    break

        return first_child

    def _remove_comp_from_list(self, comp_list: List[cass_client.Competency], comp_item: cass_client.Competency):
        id_to_find = comp_item.id
        deletion_idx = None  # Need to use a var so we don't delete during iteration
        for idx, comp in enumerate(comp_list):
            if comp.id == id_to_find:
                deletion_idx = idx
        if deletion_idx is not None:
            comp_list.pop(deletion_idx)
        else:
            # This has been known to throw errors, but if we can't delete an item using pop, not sure what else to do ¯\_(ツ)_/¯
            comp_list.remove(comp_item)

    def get_relations(self, relation_type=None, source=None, target=None):
        # We want to exclude relations that (for whatever reason) have both ends pointing to the same node
        # A competency requires/enables itself? Makes no sense
        filtered_values = [relation for relation in self.relation_objs.values() if relation.target != relation.source]
        if relation_type is not None:
            allowed_values = ["narrows", "requires", "desires", "isEnabledBy", "isRelatedTo", "isEquivalentTo"]
            if relation_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `relation_type` ({0}), must be one of {1}"  # noqa: E501
                        .format(relation_type, allowed_values)
                )
            filtered_values = [relation for relation in filtered_values if relation.relation_type == relation_type]

        if source is not None:
            if hasattr(source, '__iter__') and type(source) is not str:
                filtered_values = [relation for relation in filtered_values if relation.source in source]
            else:
                filtered_values = [relation for relation in filtered_values if relation.source == source]

        if target is not None:
            if hasattr(target, '__iter__') and type(target) is not str:
                filtered_values = [relation for relation in filtered_values if relation.target in target]
            else:
                filtered_values = [relation for relation in filtered_values if relation.target == target]

        return filtered_values

    def competency_to_str_with_children(self, competency: cass_client.Competency, indent_string=""):
        output_str = indent_string + self.competency_to_str(competency) + '\n'
        child = getattr(competency, "first_child", None)
        while child is not None:
            output_str += self.competency_to_str_with_children(child, indent_string + "    ")
            child = getattr(child, "next_neighbor", None)
        return output_str

    def competency_to_str(self, competency: cass_client.Competency):
        prev_neighbor = self.get_previous_neighbor(competency)
        next_neighbor = self.get_next_neighbor(competency)
        return '{}{}: {} ({}), prev_neighbor: {}, next_neighbor: {}, requires: {}'.format(
            '' if competency.dctermstype is None else competency.dctermstype + ' ',
            competency.ceasncoded_notation,
            competency.name,
            competency.id,
            'None' if prev_neighbor is None else prev_neighbor.name,
            'None' if next_neighbor is None else next_neighbor.name,
            [r.ceasncoded_notation for r in self.get_required_competencies(competency)]
        )

    def get_id_from_url(self, url: str):
        # If the ID of an object comes in as a url, we sometimes only want the actual ID on the end of it
        # This slice will work as intended whether the string is a url or not, so it can be used as a catch-all
        while url[-1] == "/":
            url = url[:-1]
        # if rfind doesn't find any slashes, we get url[0:], thus the slice returns the whole list
        return url[url.rfind("/") + 1:]

    # --- Primary external-use functions ---

    def get_obj_by_id(self, id_or_url) -> Optional[cass_client.Competency]:
        for key in self.competency_objs.keys():
            if self.get_id_from_url(key) == self.get_id_from_url(id_or_url):
                return self.competency_objs[key]
        return None

    def get_all_top_level_competencies(self) -> Dict[str, cass_client.Competency]:
        return self.top_level_competencies

    def get_first_top_level_competency(self) -> cass_client.Competency:
        return self.first_top_level_competency

    def get_children(self, competency: cass_client.Competency) -> Optional[List[cass_client.Competency]]:
        children = getattr(competency, "children")
        return children.values() if children else None

    def get_unblocked_unmastered_ancestors(self, competency: cass_client.Competency, mastered_competency_ids: List[str], only_leaves: bool=False) -> List[cass_client.Competency]:
        ancestors = []
        self._get_unblocked_unmastered_ancestors(competency, ancestors, self._cleanse_ids(mastered_competency_ids), only_leaves)
        return ancestors

    def _get_unblocked_unmastered_ancestors(self, competency: cass_client.Competency,
                                              ancestors: List[cass_client.Competency],
                                              mastered_competency_ids: List[str], only_leaves: bool):
        if self.is_leaf(competency):
            competency = self.get_parent_competency(competency)

        if len(self.get_required_competencies(competency)) == 0:
            ancestors.extend(self.get_unblocked_unmastered_descendants(competency, mastered_competency_ids, only_leaves))
        else:
            for required in self.get_required_competencies(competency):
                self._get_unblocked_unmastered_ancestors(required, ancestors, mastered_competency_ids, only_leaves)

    def _is_mastered(self, competency: cass_client.Competency, cleansed_mastery_ids: List[str]):
        return competency.id in cleansed_mastery_ids

    def is_mastered(self, competency: cass_client.Competency, mastery_ids: List[str]):
        return self._is_mastered(competency, self._cleanse_ids(mastery_ids))

    def get_unblocked_unmastered_descendants(self, competency: cass_client.Competency, mastered_competency_ids: List[str], only_leaves: bool=False) -> List[cass_client.Competency]:
        descendants = []
        self._get_unblocked_unmastered_descendants(competency, descendants, self._cleanse_ids(mastered_competency_ids), only_leaves)
        return descendants

    def _get_unblocked_unmastered_descendants(self, competency: cass_client.Competency,
                                                          descendants: List[cass_client.Competency],
                                                          mastered_competency_ids: List[str], only_leaves: bool):
        # TODO: This is tightly coupled to the "TLA 2018 July Framework" Cass Framework
        # It relies on the fact that leaf nodes have no "requires" relationship in this framework, and instead depend
        # on their parent's requires relationship. This code also relies on using get_previous_neighbor() to get the
        # the required node for nodes that have a required relationship. In the framework, there is max of one requires
        # relationship per child node (i.e. a node can only require one other node). If this changes, and a node can
        # require multiple nodes, then get_previous_neighbor() will not work.
        children = self.get_children(competency)
        if children is not None:
            for child in children:
                if child.id not in mastered_competency_ids:
                    if self.is_leaf(child):
                        # get parent to find requires relationship
                        parent = self.get_parent_competency(child)

                        if self._prerequisites_met(parent, mastered_competency_ids):
                            descendants.append(child)
                    else:
                        if not only_leaves:
                            requires = self.get_required_competencies(child)
                            if self._prerequisites_met(child, mastered_competency_ids):
                                descendants.append(child)
                        self._get_unblocked_unmastered_descendants(child, descendants, mastered_competency_ids, only_leaves)

    def is_leaf(self, competency: cass_client.Competency):
        return self.get_children(competency) is None and len(self.get_required_competencies(competency)) == 0

    def get_descendants(self, competency: cass_client.Competency) -> Optional[List[cass_client.Competency]]:
        descendants = []
        self._get_descendants(competency, descendants)
        return descendants

    def _get_descendants(self, competency: cass_client.Competency, descendants: List[cass_client.Competency]):
        children = self.get_children(competency)
        if children is not None:
            descendants.extend(children)
            for child in children:
                self._get_descendants(child, descendants)

    # The get_children function would apparently at times give the children in reversed order
    # This function guarantees the order, though it takes longer to run
    def get_children_ordered(self, competency: cass_client.Competency) -> Optional[List[cass_client.Competency]]:
        first_child = self.get_first_child(competency)
        if first_child is None:
            return None
        children = [first_child]
        next_child = self.get_next_neighbor(first_child)
        while next_child is not None:
            children.append(next_child)
            next_child = self.get_next_neighbor(next_child)
        return children

    def get_first_child(self, competency) -> cass_client.Competency:
        return getattr(competency, "first_child", None)

    def get_next_neighbor(self, competency: cass_client.Competency) -> Optional[cass_client.Competency]:
        return getattr(competency, "next_neighbor", None)

    def get_previous_neighbor(self, competency: cass_client.Competency) -> Optional[cass_client.Competency]:
        return getattr(competency, "prev_neighbor", None)

    def get_required_competencies(self, competency: cass_client.Competency) -> List[cass_client.Competency]:
        return getattr(competency, "requires", None)

    def get_parent_top_level_competency(self, competency: cass_client.Competency):
        competency = competency
        while getattr(competency, "parent", None):
            competency = self.get_parent_competency(competency)
        return competency

    def get_parent_competency(self, competency: cass_client.Competency) -> Optional[cass_client.Competency]:
        parent = getattr(competency, "parent", None)
        if parent:
            return parent
        return None

    def get_next_in_chain(self, competency: cass_client.Competency) -> Optional[cass_client.Competency]:
        # Priority in order is children->neighbors->next parent

        first_child = self.get_first_child(competency)
        if first_child:
            return first_child

        next_neighbor = self.get_next_neighbor(competency)
        if next_neighbor:
            return next_neighbor

        parent = self.get_next_neighbor(self.get_parent_competency(competency))
        if parent:
            return parent

        return None

    def get_competency_chain(self, competency: cass_client.Competency) -> List[cass_client.Competency]:
        chain = []
        current_member = self.get_next_in_chain(competency)
        while current_member is not None and getattr(current_member, "parent", None) is not None:
            chain.append(current_member)
            current_member = self.get_next_in_chain(current_member)
        return chain

    def get_entire_chain(self, competency: cass_client.Competency = None):
        if competency is None:
            competency = self.get_first_top_level_competency()
        chain = []
        current_member = competency
        while current_member is not None:
            chain.append(current_member)
            current_member = self.get_next_in_chain(current_member)
        return chain

    def prerequisites_met(self, competency: cass_client.Competency, mastery_ids: List[str]):
        mastery_ids = self._cleanse_ids(mastery_ids)
        if self.is_leaf(competency):
            return self._prerequisites_met(self.get_parent_competency(competency), mastery_ids)
        return self._prerequisites_met(competency, mastery_ids)

    def _prerequisites_met(self, competency: cass_client.Competency, cleansed_mastery_ids: List[str]):
        requires = self.get_required_competencies(competency)
        required_ids = [r.id for r in requires]
        return all(rid in cleansed_mastery_ids for rid in required_ids)

    def _cleanse_ids(self, competency_ids: List[str]):
        cleansed = []
        for mid in competency_ids:
            competency = self.get_obj_by_id(mid)
            if competency is not None:
                cleansed.append(competency.id)
        return cleansed


if __name__ == '__main__':
    cass_graph = CassGraph("603d5ac2-fa9e-43c3-9c50-87ff65804ccd")
    print(str(cass_graph))
