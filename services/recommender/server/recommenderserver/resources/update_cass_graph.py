import pickle

from cass_graph_client.cass_graph import CassGraph
from os import path


def update_cass_graph_resource(framework_id: str):
    cass_graph = CassGraph(framework_id)
    cass_graph_pickle_file = path.join(path.abspath(path.dirname(__file__)), 'CassGraph_' + framework_id + '.pkl')
    file = open(cass_graph_pickle_file, 'wb')
    pickle.dump(cass_graph, file)
    file.close()
    print('Updated cass graph pickle file -> {}'.format(cass_graph_pickle_file))

if __name__ == '__main__':
    update_cass_graph_resource('603d5ac2-fa9e-43c3-9c50-87ff65804ccd')