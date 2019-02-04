<template>
  <li>
    <v-container fluid class="pa-0">
      <v-layout row>
        <v-flex xs12 sm8 md4>
          <competency-item
            :competency="competency"
            :toggle="toggle"
            :open="open"
            :mastery="mastery"
            :headNode="this.headNode"
          />
        </v-flex>
      </v-layout>
    </v-container>
    <ul v-show="open" v-if="isFolder">
      <item
        class="item"
        v-for="(competency, index) in competency.children"
        :key="index"
        :competency="competency"
        :masteryProbabilities="masteryProbabilities"
        :headNode="false">
      </item>
    </ul>
  </li>
</template>

<script>
import CompetencyItem from '@/components/tiles/CompetencyItem'
export default {
  name: 'item',
  props: {
    competency: Object,
    masteryProbabilities: Object,
    headNode: Boolean
  },
  data: function () {
    return {
      open: true
    }
  },
  computed: {
    isFolder: function () {
      return this.competency.children &&
        this.competency.children.length
    },
    mastery: function() {
      let competencyId = this.competency['@id']
      if (this.masteryProbabilities == null || Object.keys(this.masteryProbabilities).length === 0 || !(competencyId in this.masteryProbabilities)) return '0%'

      var masteryProbability = this.masteryProbabilities[competencyId]
      masteryProbability = Math.round(parseFloat(masteryProbability)*100)
      return masteryProbability + "%"
    }
  },
  methods: {
    toggle: function () {
      if (this.isFolder) {
        this.open = !this.open
      }
    }
  },
  components: {
    'competency-item': CompetencyItem
  }
}
// https://vuejs.org/v2/examples/tree-view.html
</script>

<style>
.bold {
  font-weight: bold;
  cursor: pointer;
}
ul {
  padding-left: 2em;
  list-style-type: none;
}
</style>
