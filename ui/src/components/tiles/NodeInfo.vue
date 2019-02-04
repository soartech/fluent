<template>
  <v-card>
    <v-container fluid>
      <v-layout row class="pa-2">
        <v-flex xs12>
          <h2><img v-if="isNodeBadge" style="height: 15px;" src="static/img/icons/gold-police-badge-icon-9.png"/>  {{ nodeName }}</h2>
        </v-flex>
      </v-layout>
      <v-layout row class="pa-2">
        <v-flex xs12>
          <h3 style="font-weight: normal; font-style: italic;">{{ nodeDescription }}</h3>
        </v-flex>
      </v-layout>
      <v-layout row wrap class="pa-2" text-xs-right> 
        <v-spacer/>
        <v-flex xs12>
          <v-btn color="green" v-if="node !== null && userGoal === node['@id']">Selected</v-btn>
          <v-btn v-else @click="setGoal()">Set Goal</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
export default {
  props: {
    node: Object,
    d3Nodes: Object,
    d3Update: Function
  },
  data () {
    return {
    }
  },
  methods: {
    async setGoal() {
      this.$store.commit('setLearnerGoal', this.node['@id'])
      let result = await this.$store.dispatch('patchLearnerGoal', this.$store.state.userInfo.goal);
      console.log("Set learner goal to" + this.$store.state.userInfo.goal);
      this.d3Update(this.d3Nodes)
    }
  },
  computed: {
    userGoal () {
      return this.$store.state.userInfo.goal
    },
    isNodeBadge () {
      if (this.node != null) return this.node.parents.length === 0
      return 'N/A'
    },
    nodeName () {
      if (this.node != null) return this.node.name
      return 'N/A'
    },
    nodeDescription () {
      // They include the title of the competency in the description, so I wrote a hacky way to remove that for display.
      if (this.node != null) {
        console.log(this.node)
        if (!('description' in this.node) || this.node.description === null || this.node.description === '') return 'No description present'
        let nodeDescriptionParts = this.node.description.split(':')
        if (nodeDescriptionParts.length <= 1) {
          return this.node.description
        }
        return nodeDescriptionParts.slice(1, nodeDescriptionParts.length).join(' ').trim()
      }
      return 'N/A'
    }
  }
}
</script>
