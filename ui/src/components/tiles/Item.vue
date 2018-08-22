<template>
  <li>
    <v-container fluid class="pa-0">
      <v-layout row>
        <v-flex xs12 sm8 md4>
          <competency-item
            :competency="competency"
            :toggle="toggle"
            :open="open"
            :held="isHeld"
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
        :masteryEstimates="masteryEstimates">
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
    masteryEstimates: Object
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
    isHeld: function () {
      let competencyId = this.competency['@id']
      if (competencyId in this.masteryEstimates && this.masteryEstimates[competencyId] === 'held') {
        return true
      } else {
        return false
      }
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
