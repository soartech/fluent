<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <h2>Graphical Skill Tree</h2>
      </v-flex>
    </v-layout>
    <v-layout v-if="!competenciesReady" row>
      <v-spacer/>
      <v-flex xs11 sm6 md5 lg3>
        <loading-tile
        :loadingText="'Loading Competency Structure'"/>
      </v-flex>
      <v-spacer/>
    </v-layout>
    <v-layout row>
      <v-flex xs10 ref='graphTarget' text-xs-center>
      </v-flex>
      <v-flex xs2>
        <v-card>
          <v-container fluid>
            <v-layout row>
              <v-flex xs6>
                <h3>Key</h3>
              </v-flex>
              <v-flex xs6 text-xs-right>
                <h3><span class="text-button" style="cursor: pointer; padding: 2px;" @click="hideShowKey()">{{keyButtonText}}</span></h3>
              </v-flex>
            </v-layout>
            <div :class="!keyExpanded ? 'hidden-thing': ''">
              <v-divider style="margin-top: 5px; margin-bottom: 5px;"/>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:selectedNode">
                  <!-- Selected Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;">Selected Node</h3>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:goalNode">
                  <!-- Goal Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;" >Goal Node</h3>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:goalParentNode">
                  <!-- Goal Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;" >Goal Parent Node</h3>
                </v-flex>
              </v-layout>
              <v-divider style="margin-top: 5px; margin-bottom: 5px;"/>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:noviceNode">
                  <!-- Novice Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;" >Started</h3>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:intermediateNode">
                  <!-- Intermediate Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;" >In Progress</h3>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:expertNode">
                  <!-- Expert Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;" >Ready</h3>
                </v-flex>
              </v-layout>
              <v-divider style="margin-top: 5px; margin-bottom: 5px;"/>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:openNode">
                  <!-- Novice Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;" >Expanded Node</h3>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs2 style="text-align: center;" ref="key:closedNode">
                  <!-- Intermediate Node -->
                </v-flex>
                <v-flex xs10>
                  <h3 style="font-weight: normal;" >Minimized Node</h3>
                </v-flex>
              </v-layout>
            </div>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xs12>
        <node-info
        v-if="selectedNode != null"
        :node="selectedNode"
        :d3Nodes="d3Nodes"
        :d3Update="updateNodeOutlines"/>
      </v-flex>
    </v-layout>
  </v-container>
</template>


<script>
import * as d3 from 'd3';
import NodeInfo from '@/components/tiles/NodeInfo'
import LoadingTile from '@/components/tiles/LoadingTile'
const data = [99, 71, 78, 25, 36, 92];

export default {
  name: 'competency-tree',
  data () {
    return {
      selectedNode: null,
      graphCreated: false,
      d3Nodes: null,
      masteryColors: {
        'expert': '#616161',
        'intermediate': '#9E9E9E',
        'novice': '#E0E0E0'
      },
      insideTextColors: {
        'expert': 'rgb(236, 236, 234)',
        'intermediate': '#000',
        'novice': '#000'
      },
      colors: [],
      d3Text: null,
      d3Indicators: null,
      wordWrapFunc: null,
      separationLevel: null,
      keyExpanded: true,
      keyButtonText: "-"
    }
  },
  mounted() {
    this.graphCreated = false
    this.createGraph()
  },
  computed: {
    userGoal () {
      return this.$store.state.userInfo.goal
    },
    goalNodeParents () {
      var foundNodeIds = []
      if (this.userGoal !== '' && this.competencies != null && this.userGoal in this.competencies) {
        let currentCompetency = this.competencies[this.userGoal]
        console.log('Attempting to find parent nodes')
        var parents = currentCompetency.parents
        while (parents != null && parents.length > 0) {
          var tempParents = []
          for (var idx in parents) {
            console.log("Iterating through parents")
            var competency = this.competencies[parents[idx]]
            var compParents = competency.parents
            if (compParents != null && compParents.length > 0) {
              tempParents = tempParents.concat(compParents)
            } 
            
            foundNodeIds.push(competency['@id'])
          }
          parents = tempParents
        }
      }
      return foundNodeIds
    },
    competenciesReady () {
      let competencies = this.competencies
      if (Object.keys(competencies).length > 0) {
        this.createGraph()
        return true
      }

      return false
    },
    competencies() {
      return this.$store.state.competencyMappings;
    },
    relationsReady() {
      let relations = this.relations;
      if (relations.length > 0) {
        return true;
      }
      return false;
    },
    relations() {
      return this.$store.state.relations;
    },
    currentNode () {
      return {
        name: 'Placeholder Name',
        tlo: 'Placeholder TLO',
        elo: 'Placeholder ELO'
      }
    },
    stateMasteryEstimates () {
      return this.$store.state.userInfo.masteryEstimates
    },
    stateMasteryProbabilities () {
      return this.$store.state.userInfo.masteryProbabilities
    },
    masteryEstimates () {
      let masteryEstimates = this.stateMasteryEstimates
      var mapping = {}
      for (var estIdx in masteryEstimates) {
        let key = masteryEstimates[estIdx].competencyId
        mapping[key] = masteryEstimates[estIdx].mastery
      }
      return mapping
    },
    masteryProbabilities () {
      let masteryProbabilities = this.stateMasteryProbabilities
      var mapping = {}
      var timeMapping = {}
      for (var probIdx in masteryProbabilities) {
        let key = masteryProbabilities[probIdx].competencyId
        if (masteryProbabilities[probIdx].source === 'CASS') {
          if (key in mapping) {
            var prevTime = Date.parse(timeMapping[key])
            var currentTime = Date.parse(masteryProbabilities[probIdx].timestamp)
            if (currentTime > prevTime) {
              mapping[key] = masteryProbabilities[probIdx].probability
              timeMapping[key] = masteryProbabilities[probIdx].timestamp
            }
          } else {
            mapping[key] = masteryProbabilities[probIdx].probability
            timeMapping[key] = masteryProbabilities[probIdx].timestamp
          }
        }
      }
      return mapping
    }
  },
  watch: {
    userGoal: function (value) {
      this.updateNodeOutlines()
    },
    goalNodeParents: function (value) {
      this.updateNodeOutlines()
    },
    masteryEstimates: function (value) {
      this.updateMasteryEstimates()
      this.updateNodeInsideText()
    },
    masteryProbabilities: function (value) {
      this.updateMasteryProbability()
    }
  },
  methods: {
    hideShowKey () {
      this.keyExpanded = !this.keyExpanded
      if (this.keyButtonText === '-') this.keyButtonText = '+'
      else if (this.keyButtonText === '+') this.keyButtonText = '-'
    },
    createGraph () {
      if (Object.keys(this.competencies).length == 0 || this.graphCreated) 
      {
        console.log("Skipping graph creation")
        return
      }
      this.graphCreated = true

      var lastGraphState = sessionStorage.getItem("lastGraphState");
      if (lastGraphState == null) {
        lastGraphState = JSON.parse('{}');
      }
      else {
        lastGraphState = JSON.parse(lastGraphState);
      }

      var badgeNumber = 0; //idx of top level comp

      var competencies = JSON.parse(JSON.stringify(this.competencies));
      var relations = JSON.parse(JSON.stringify(this.relations));

      for(var id in competencies) {
        competencies[id]['id'] = competencies[id]['@id'];
      }

      competencies = Object.keys(competencies).map(function(key){
          return competencies[key];
      });
        
      var freezeMultipleNodes = true;
      var freezeSimOnDrag = false;
      var doWordWrap = true;

      var width = 1020,
          height = 450,
          bigRadius = 14;

      var separationLevel;

      var svg = d3.select(this.$refs['graphTarget']).append("svg")
          .attr("width", width)
          .attr("height", height);

      var arrowColor = {"gray":"rgb(153, 153, 153)", "salmon":"rgb(228, 158, 160)" };

      svg.append('defs').append('marker')
              .attr('id','arrowheadGray')
              .attr('viewBox','-0 -5 10 10')
              .attr('refX',13)
              .attr('refY',0)
              .attr('orient','auto')
              .attr('markerWidth',3)
              .attr('markerHeight',3)
              .attr('xoverflow','visible')
              .append('svg:path')
              .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
              .attr('fill', arrowColor["gray"])
              .style('stroke','none');

      
      svg.select('defs').append('marker')
              .attr('id','arrowheadSalmon')
              .attr('viewBox','-0 -5 10 10')
              .attr('refX',13)
              .attr('refY',0)
              .attr('orient','auto')
              .attr('markerWidth',3)
              .attr('markerHeight',3)
              .attr('xoverflow','visible')
              .append('svg:path')
              .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
              .attr('fill', arrowColor["salmon"])
              .attr('opacity', 0.3)
              .style('stroke','none');
      var prevNode;

      let graphNodes = competencies;
      let graphLinks = relations;

      var node, text, link, indicators;

      //var color = d3.scaleOrdinal(d3.schemeCategory20);
      var color = ['#FAFAFA', '#E0E0E0', '#9E9E9E', '#616161', '#212121'];
      this.colors = color
      var masteryColors = {
        'expert': '#616161',
        'intermediate': '#9E9E9E',
        'novice': '#E0E0E0'
      }

      d3.select(this.$refs['key:selectedNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode selectedNode")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", color[0]);
            
      d3.select(this.$refs['key:goalParentNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode parentNode")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", color[0]);
      d3.select(this.$refs['key:goalNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode goalNode")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", color[0]);
      d3.select(this.$refs['key:noviceNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode node")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", masteryColors['novice']);
      d3.select(this.$refs['key:intermediateNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode node")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", masteryColors['intermediate']);
      d3.select(this.$refs['key:expertNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode node")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", masteryColors['expert']);

      d3.select(this.$refs['key:closedNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode node")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", color[0]);
      
      d3.select(this.$refs['key:closedNode'])
        .select("svg")
          .append("text")
            .attr("dx", bigRadius - 4)
            .attr("dy", 18)
            .style('font-size', '14px')
            .text('+');

      d3.select(this.$refs['key:openNode'])
        .append("svg")
          .attr("width", bigRadius * 2)
          .attr("height", bigRadius * 2)
          .attr("class", "legendNode node")
          .append("circle")
            .attr("r", bigRadius - 5)
            .attr("cx", bigRadius)
            .attr("cy", bigRadius)
            .attr("fill", color[0]);
      
      d3.select(this.$refs['key:openNode'])
        .select("svg")
          .append("text")
            .attr("dx", bigRadius - 2)
            .attr("dy", 18)
            .style('font-size', '14px')
            .text('-');

      var simulation = d3.forceSimulation();

      //Physics to run every tick
      function ticked() {
          node.selectAll("circle")
              .attr("cx", function(d)
                { 
                  d.x = 30 + (separationLevel * d.level)
                  return d.x = Math.max(bigRadius, Math.min(width - bigRadius, d.x)); 
                })
              .attr("cy", function(d) { return d.y = Math.max(bigRadius, Math.min(height - bigRadius, d.y)); });
          text.selectAll("text")
              .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
          
          indicators.selectAll('text')
              .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })

          link.selectAll('line')
              .attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });
      }

      //Establish nodes and links to be involved in physics processing
      //Must be called each time new nodes are added to the SVG
      function setSimLinksAndNodes() {
        simulation
            .nodes(graphNodes)
            .on("tick", ticked);

        simulation.force("link").links(graphLinks);
      }

      function turnPhysicsOn() {
        simulation.force("link", d3.forceLink().distance(0).id(function(d) { return d.id; }).strength(0));
        if (typeof graphLinks !== "undefined" && typeof graphNodes !== "undefined")
          setSimLinksAndNodes();
      }

      function getExistingNodeIDs() {
        var existingNodeIDs = [];
        node.selectAll('g').each(function(d) {existingNodeIDs.push(d.id);});
        return existingNodeIDs;
      }

      function filterLinks(d, clickedNode, level) {
        var existingNodeIDs = getExistingNodeIDs();

        if (typeof d.target == 'string') {
          return existingNodeIDs.includes(d.target) && existingNodeIDs.includes(d.source);
        }
        else {
          return existingNodeIDs.includes(d.target.id) && existingNodeIDs.includes(d.source.id);
        }
      }

      function filterNodesLessThan(d, clickedNode, level) {
        if (clickedNode == null)
          return d.level <= level;

        return (d.level <= level) && d3.select(clickedNode.parentNode).data()[0]['children'].includes(d.id); //Getting data from a circle
      }

      function filterNodes(d, clickedNode, level) {

        if (clickedNode == null)
          return d.level == level;

        return (d.level == level) && d3.select(clickedNode.parentNode).data()[0]['children'].includes(d.id) && (findExistingNode(d.id) == null); 
      }

      function filterExistingNodes(idString) {
        var nodeExists = false;
        node.selectAll('g').each(function (d) {
          if (d.id == idString) {
            nodeExists = true;
            return;
          }
        })
        return nodeExists;
      }

      function filterText(d, clickedNode, level) {
        if (clickedNode == null)
          return d.level == level;

        return (d.level == level) && d3.select(clickedNode.parentNode).data()[0]['children'].includes(d.id); 
      }
      function filterIndicators(d, clickedNode, level) {
        if (clickedNode == null)
          return d.level == level;

        return (d.level == level) && d3.select(clickedNode.parentNode).data()[0]['children'].includes(d.id); 
      }

      function nodeDoubleClick(node, d, instance) {
        if (d3.select(node).attr("expanded") == "true") {
          removeChildNodes(node);
          indicators.selectAll("g").filter(function (c) {return c['@id'] === d['@id']}).select("text").text("+").attr('dx', -4)
          d3.select(node).attr("expanded", "false"); 
          setNodeSpacing();
        }
        else if (d3.select(node).attr("expanded") == "false" && d.children.length > 0) {
          if (!(d.level.toString() in lastGraphState)) {
            lastGraphState[d.level.toString()] = [d['@id']];
          }
          else if (lastGraphState[d.level.toString()].indexOf(d['@id']) == -1){
            lastGraphState[d.level.toString()].push(d['@id']);
          }
          sessionStorage.setItem("lastGraphState", JSON.stringify(lastGraphState));

          indicators.selectAll("g").filter(function (c) {return c['@id'] === d['@id']}).select("text").text("-").attr("dx", -2)

          d3.select(node).attr("expanded", "true");
          plotNodesOfLevel(node, d.level + 1, instance);
        }
      }

      //Plots all nodes of a certain level that are children of clickedNode
      //If clickedNode is null, as it is when called by the json reader,
        //all of the nodes at the specified level will be plotted unconditionally
      //In the future we could add optional behavior for if level is null,
        //where we would then plot all children regardless of the level.
        //Though this has the effect of fully expanding the tree if clickedNode is root,
        //since the top level nodes seem to have "narrows" relations with all of their children
      function plotNodesOfLevel(clickedNode, level, instance) {

        
        node
          .selectAll("g")
          .data(graphNodes.filter(function(d) {return filterNodes(d, clickedNode, level);}), function(d){return d.id;})
          .enter().append("g")
            .attr("class", function (d) {
              if (instance.userGoal !== null && instance.userGoal === d['@id']) return "goalNode"
              else if (instance.userGoal !== null && instance.goalNodeParents != null && instance.goalNodeParents.indexOf(d['@id']) >= 0) return "parentNode"
              return "node"
            })
            .attr("id", "lvl-" + level)
            .append("circle")
              .attr("r", bigRadius)
              .attr("fill", function(d) { 
                
                if (d['@id'] in instance.masteryEstimates) {
                  let masteryEstimate = instance.masteryEstimates[d['@id']]
                  if (masteryEstimate !== null && masteryEstimate in masteryColors) {
                    return masteryColors[masteryEstimate]
                  }
                }
                return color[0]; }) //Use this to set color based on mastery
              .attr("expanded", "false")
              .on("mouseover", function(d) {
                var correspondingTextNode = findExistingNodeText(d.id);
                var text = d3.select(correspondingTextNode).select("tspan").text();
                d3.select(correspondingTextNode).select("tspan").text(function (d) {
                  var masteryProbability = instance.getMasteryProbabilityById(d['@id'])
                  if (masteryProbability === null) {
                    masteryProbability = '0'
                  }
                  masteryProbability = parseFloat(masteryProbability)
                  masteryProbability = Math.round(masteryProbability*100)
                  if (text != "("+masteryProbability+"%) " + d.name) return text.slice(0, -3)
                  return text
                });
                d3.select(correspondingTextNode).selectAll("tspan").style("visibility", "visible");
              })
              .on("mouseout", function(d) {
                var correspondingTextNode = findExistingNodeText(d.id);
                var firstLine = true;
                var text = d3.select(correspondingTextNode).select("tspan").text();
                d3.select(correspondingTextNode).select("tspan").text(function (d) {
                  var masteryProbability = instance.getMasteryProbabilityById(d['@id'])
                  if (masteryProbability === null) {
                    masteryProbability = '0'
                  }
                  masteryProbability = parseFloat(masteryProbability)
                  masteryProbability = Math.round(masteryProbability*100)
                  if (text != "("+masteryProbability+"%) " + d.name) return text + '...'
                  return text
                });
                d3.select(correspondingTextNode).selectAll("tspan").style("visibility", function() {if (firstLine) {firstLine = false; return "visible";} else {return "hidden";}});
              })
              .on("click", function(d) {
                  instance.d3Nodes = node
                  instance.d3Text = text
                  instance.d3Indicators = indicators
                  instance.selectedNode = d3.select(this).data()[0]
                  resetClasses(instance)
                  d3.select(this.parentNode).attr("class", "selectedNode")
                  d3.event.stopPropagation();
                })
              .on('dblclick', function (d) {
                nodeDoubleClick(this, d, instance);
                d3.event.stopPropagation();
              })
              .on("contextmenu", function(d) {d3.event.preventDefault(); d.fx = null; d.fy = null;})
              .call(d3.drag()
                  .on("start", dragstarted)
                  .on("drag", dragged)
                  .on("end", dragended));
        instance.d3Nodes = node;

        simulation
          .nodes(graphNodes)
          .on("tick", ticked);
        setNodeSpacing(level);

        link
          .selectAll("line")
          .data(graphLinks.filter(function(d) {return filterLinks(d, clickedNode, level);}), function(d){return d['@id'];})
          .enter().append("line")
            .attr('class', 'link')
            .attr("stroke", function(d) {return d.relationType == "narrows" ? arrowColor["salmon"] : arrowColor["gray"]})
            .attr("stroke-opacity", function(d) {return d.relationType == "narrows" ? 0.3 : 0.6;})
            .attr("id", "lvl-" + level)
            .attr("stroke-width", function(d) { return 5/*return Math.sqrt(d.value);*/ })
            .attr('marker-end', function(d) {return d.relationType == "narrows" ? "url(#arrowheadSalmon)" : "url(#arrowheadGray)";});
            
      

        text
          .selectAll("g")
          .data(graphNodes.filter(function(d) {return filterText(d, clickedNode, level);}), function(d){return d.id;})
          .enter().append("g")
            .attr("class","label")
            .attr("id", "lvl-" + level)
            .append("text")
            .attr("dx", 18)
            .attr("dy", ".35em")
            .style('font-size', '12px')
            .text(function(d) { 
              var masteryProbability = instance.getMasteryProbabilityById(d['@id'])
                  if (masteryProbability === null) {
                    masteryProbability = '0'
                  }
              masteryProbability = parseFloat(masteryProbability)
              masteryProbability = Math.round(masteryProbability*100)
              return "("+masteryProbability+"%) " + d.name; })
            .call(wordWrap, separationLevel, instance);

        indicators
          .selectAll("g")
          .data(graphNodes.filter(function(d) {return filterIndicators(d, clickedNode, level);}), function(d){return d.id;})
          .enter().append("g")
            .attr("class","label")
            .attr("id", "lvl-" + level)
            .append("text")
            .attr("dx", -4)
            .attr("dy", ".35em")
            .style('font-size', '14px')
            .attr('fill', function (d) {
              if (d['@id'] in instance.masteryEstimates) {
                let masteryEstimate = instance.masteryEstimates[d['@id']]
                if (masteryEstimate !== null && masteryEstimate in instance.insideTextColors) {
                  return instance.insideTextColors[masteryEstimate]
                }
              }
              return instance.insideTextColors["novice"]
            })
            .text(function(d) {
              if (d.children != null && d.children.length > 0) return "+"
              return ""; });

        instance.d3Text = text
        instance.d3Indicators = indicators
        simulation.alpha(0.1);
      }

      function resetClasses(instance) {
        node
          .selectAll("g")
          .attr("class", function (d) {
            if (instance.userGoal !== null && instance.userGoal === d['@id']) return "goalNode"
            else if (instance.userGoal !== null && instance.goalNodeParents != null && instance.goalNodeParents.indexOf(d['@id']) >= 0) return "parentNode"
            return "node"
          })
      }
      //Remove all links that were attached to a given node being deleted
      function removeLinks(deletedNode) {
        // var childrenIDs = d3.select(deletedNode).data()[0]['children'];
        var nodeIdString = d3.select(deletedNode).data()[0]['id'];
        // var parentLevel = d3.select(deletedNode).data()[0]['level'];
        link.selectAll('line').each(function(d) {
          if (d.target.id == nodeIdString || d.source.id == nodeIdString) {
            d3.select(this).remove();
          }
        })  
      }

      //Recursively remove all child nodes from a clicked node
      //Does not remove clickedNode
      function removeChildNodes(clickedNode) {
        var clickedNodeData = d3.select(clickedNode).data()[0];
        var parentLevel = clickedNodeData['level'];
        var parentIdString = clickedNodeData['id'];

        if (parentLevel.toString() in lastGraphState) {
          var idxOfItem = lastGraphState[parentLevel.toString()].indexOf(parentIdString);
          if (idxOfItem > -1) {
            lastGraphState[parentLevel.toString()].splice(idxOfItem, 1);
          }
        }
        sessionStorage.setItem("lastGraphState", JSON.stringify(lastGraphState));

        //var childrenIDs = d3.select(clickedNode).data()[0]['children'];
        var children = node.selectAll("g#lvl-" + (parentLevel + 1)).selectAll("circle");
        
        
        children.each(function(d)
        { 
          
          var childIdString = d.id;
          //var childNode = findExistingNode(childIdString);
          var childNodeText = findExistingNodeText(childIdString);
          var childNodeIndicator = findExistingNodeIndicator(childIdString);
          if (this != null && d['parents'].includes(parentIdString)) {

            var doDeleteNode = true;
            var parentsList = d['parents'];
            
            for (var i = 0; i < parentsList.length; i++) {
              var currentParent = findExistingNode(parentsList[i]);
              if (currentParent == undefined) {
                console.log("Current parent was null");
              }
              
              if (currentParent != null 
                && d3.select(currentParent).data()[0]['id'] != parentIdString 
                && d3.select(currentParent).data()[0]['level'] == parentLevel
                && d3.select(currentParent).select("circle").attr("expanded") == "true")
              {
                doDeleteNode = false;
                break;
              }
            }
            if (doDeleteNode) {
              removeLinks(this);
              removeChildNodes(this);
              d3.select(this.parentNode).remove();
              d3.select(childNodeText).remove();
              d3.select(childNodeIndicator).remove();
            }
          }
        })
      }


      //Get a node object with a matching ID, given that ID as a string
      //Returns null if no node found with that ID
      function findExistingNode(idString) {
        var returnNode = null;
        node.selectAll('g').each(function (d) {
          if (d.id == idString) {
            returnNode = this;
            return;
          }
        })
        return returnNode;
      }

      //Gets corresponding text object.
      //Often used in parallel with findExistingNode
      function findExistingNodeText(idString) {
        var returnNodeText = null;
        text.selectAll('g').each(function (d) {
          if (d.id == idString) {
            returnNodeText = this;
            return;
          }
        })
        return returnNodeText;
      }

      function findExistingNodeIndicator(idString) {
        var returnNodeIndicator = null;
        indicators.selectAll('g').each(function (d) {
          if (d.id == idString) {
            returnNodeIndicator = this;
            return;
          }
        })
        return returnNodeIndicator;
      }

      let maxLevel;
      //Initial plotting of nodes from data
      (function() {
        var error = false;
        if (error) throw error;

        maxLevel = 0;
        for (var i = 0; i < graphNodes.length; i++) {
          var obj = graphNodes[i];
          if (obj['level'] > maxLevel)
            maxLevel = obj['level'];
        }
        
        //Positioning first layer nodes to be spread apart so their text doesn't overlap
        separationLevel = (width - 100) / (maxLevel + 1); //Buffer for text to fit in SVG

        this.d3SeparationLevel = separationLevel

        link = svg.append("g")
          .attr("class", "links")
          
        node = svg.append("g")
          .attr("class", "nodes")
      
        text = svg.append("g")
          .attr("class", "text")
          
        indicators = svg.append("g")
          .attr("class", "indicators")

        //Physics on by default. 
        turnPhysicsOn();
          
        //Plot the top level nodes
        indicators.selectAll("text").text('-').attr("dx", -2)
        plotNodesOfLevel(null, 0, this);
        
        if (node.node() != null) {
          for (var i = 0; i < maxLevel; i++) {
            if (i.toString() in lastGraphState) {
              var thisLevelNodes = lastGraphState[i.toString()];
              for (var j = 0; j < thisLevelNodes.length; j++) {
                var nodeToExpand = findExistingNode(thisLevelNodes[j]);
                nodeDoubleClick(nodeToExpand.children[0], d3.select(nodeToExpand).data()[0], this);
              }
            }
          }
        }
        



        var doWordWrap = false; //adding this here to disable text-based spacing for top-level nodes without removing corresponding code

        var topLevelNodes = node.selectAll("g#lvl-0");
        var verticalSeparation = height / (topLevelNodes.size() + 2);

        var prevTextNodeHeight = 0;
        var prevNodeY = doWordWrap ? verticalSeparation : 0;

        topLevelNodes.each(function(d, i) {
          if (i > 0) {
            prevTextNodeHeight = text.node().children[i-1].getBBox().height;
          }

          var newNodeY = doWordWrap ? Math.min(prevTextNodeHeight + bigRadius + prevNodeY, height) : verticalSeparation + prevNodeY;

          //Set positions    
          d3.select(this).select("circle").attr("cy", "" + newNodeY);
          d.y = newNodeY;

          prevNodeY = newNodeY;
        })

      }).bind(this)();

      function dragstarted(d) {

        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        if (typeof prevNode !== "undefined" && !freezeMultipleNodes) {  
          prevNode.datum().fx = null;
          prevNode.datum().fy = null;
        }
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }

      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        prevNode = d3.select(this);
        d.fx = null;
        d.fy = null;
      }

      //Wrap the lines of text to fit within a certain width
      function wordWrap(textSelection, textWidth, instance) {
        if (!doWordWrap) textWidth = width;

        textSelection.each(function() {
          var textItem = d3.select(this),
              words = textItem.text().split(/\s+/).reverse(),
              word,
              line = [],
              lineNumber = 0,
              lineHeight = 1.1, // ems
              y = textItem.attr("y"),
              dy = parseFloat(textItem.attr("dy")),
              tspan = textItem.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em").style("font-weight","normal");
          while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > (textWidth - bigRadius - 5)) {
              line.pop();
              tspan.text(line.join(" "));
              line = [word];
              tspan = textItem.append("tspan").attr("x", 0).attr("y", y).attr("dy", lineHeight + dy + "em").text(word).style("visibility", "hidden").style("font-weight","normal");
            }
          }
          var text = d3.select(this).select("tspan").text();
          d3.select(this).select("tspan").text(function (d) {
            var masteryProbability = instance.getMasteryProbabilityById(d['@id'])
            if (masteryProbability === null) {
              masteryProbability = '0'
            }
            masteryProbability = parseFloat(masteryProbability)
            masteryProbability = Math.round(masteryProbability*100)
            if (text != "("+masteryProbability+"%) " + d.name) return text + "..."
            return text
          });
          d3.select(this).select("tspan").style("visibility", "visible");
        });
      }

      this.wordWrapFunc = wordWrap

      function setNodeSpacing(level) {
        var startingLevel = 0;
        var endingLevel = maxLevel;
        if (level != undefined) {
          startingLevel = level;
          endingLevel = level;
        }

        for (var i = startingLevel; i <= endingLevel; i++) {
          var nodesOfLevel = node.selectAll("#lvl-" + i);
          var numNodes = nodesOfLevel.size();
          var verticalSeparation = height / (numNodes + 2);
          if (numNodes < 1) continue;
          var idx = 0;
          nodesOfLevel.each(function(d) {
            d3.select(this).select("circle")
              .each(function(d) {
                d.y = (idx + 1) * verticalSeparation;
              });
            idx++;
          })
        }

      }
    },
    updateNodeOutlines () {
      var instance = this
      if (this.d3Nodes == null) return
      this.d3Nodes
        .selectAll("g")
        .attr("class", function (d) {
          console.log("Updating node outlines")
          if (instance.userGoal !== null && instance.userGoal === d['@id']) return "goalNode"
          else if (instance.userGoal !== null && instance.goalNodeParents != null && instance.goalNodeParents.indexOf(d['@id']) >= 0) return "parentNode"
          return "node"
        })
    },
    updateNodeInsideText () {
      var instance = this
      if (this.d3Indicators == null) return

      this.d3Indicators
        .selectAll('text')
        .attr('fill', function (d) {
            if (d['@id'] in instance.masteryEstimates) {
              let masteryEstimate = instance.masteryEstimates[d['@id']]
              if (masteryEstimate !== null && masteryEstimate in instance.insideTextColors) {
                return instance.insideTextColors[masteryEstimate]
              }
            }
            return instance.insideTextColors["novice"]
        })
    },
    updateMasteryProbability () {
      var instance = this
      console.log("Updating based on mastery probability")
      if (this.d3Text == null) return
      this.d3Text
          .selectAll("g").selectAll('text')
            .text(function(d) { 
              var masteryProbability = instance.getMasteryProbabilityById(d['@id'])
                  if (masteryProbability === null) {
                    masteryProbability = '0'
                  }
              masteryProbability = parseFloat(masteryProbability)
              masteryProbability = Math.round(masteryProbability*100)
              return "("+masteryProbability+"%) " + d.name; })
            .call(instance.wordWrapFunc, instance.d3SeparationLevel, instance);
    },
    updateMasteryEstimates () {
      // Update the colors and the text.
      var instance = this
      if (this.d3Nodes == null) return
      this.d3Nodes.selectAll("g").selectAll("circle")
          .attr("fill", function(d) { 
            
            if (d['@id'] in instance.masteryEstimates) {
              let masteryEstimate = instance.masteryEstimates[d['@id']]
              if (masteryEstimate !== null && masteryEstimate in instance.masteryColors) {
                return instance.masteryColors[masteryEstimate]
              }
            }
            return instance.colors[0]; }) //Use this to set color based on mastery

      // this.d3Text
      //     .selectAll("g").selectAll('text')
      //       .text(function(d) { 
      //         var masteryEstimate = instance.getMasteryEstimateById(d['@id'])
      //             if (masteryEstimate === null) {
      //               masteryEstimate = 'novice'
      //             }
      //         return d.name + " ("+masteryEstimate+")"; })
      //       .call(instance.wordWrapFunc, instance.d3SeparationLevel, instance);
    },
    getMasteryEstimateById (competencyId) {
      if (this.masteryEstimates === null || Object.keys(this.masteryEstimates).length === 0) {
        return null
      }
      if (competencyId in this.masteryEstimates) {
        return this.masteryEstimates[competencyId]
      }

      return null
    },
    getMasteryProbabilityById (competencyId) {
      if (this.masteryProbabilities === null || Object.keys(this.masteryProbabilities).length === 0){
        return null
      }
      if (competencyId in this.masteryProbabilities) {
        return this.masteryProbabilities[competencyId]
      }

      return null
    }
  },
  created() {
  },
  components: {
    'node-info': NodeInfo,
    'loading-tile': LoadingTile
  }
};
</script>

<style>
  .node circle {
    stroke: #000;
    stroke-width: 1.5px;
  }

  .selectedNode circle {
    stroke: #ecf000;
    stroke-width: 3.5px;
  }

  .goalNode circle {
    stroke: #00c010;
    stroke-width: 3.5px;
  }

  .parentNode circle {
    stroke: #1768ff;
    stroke-width: 2.5px;
  }
  
  circle:hover {
    cursor: pointer;
  }

  .legendNode circle:hover {
    cursor: default;
  }

  text {
    pointer-events: none;
    font: 10px sans-serif;
  }

  .legend {
    border: 2px solid black;
    width: 170px;
  }

  .legend-div, h3 {
    padding-left: 10px;
  }

  .legend-entry {
    margin: 0 !important;
  }

  .legend-box {
    border: 1px solid black;
    display: inline-block;
    height: 15px;
    margin-right: .5em;
    width: 24.27px;
  }

  .salmon {
    background:rgb(228, 158, 160);
  }

  .gray {
    background:rgb(153, 153, 153);
  }

  .text-button:hover {
    background-color: #ececea
  }

  .hidden-thing {
    display: none;
  }

</style>