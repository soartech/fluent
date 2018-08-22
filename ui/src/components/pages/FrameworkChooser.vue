<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <h1>Frameworks</h1>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xs12>
        <ul id="competencyList" v-if="this.$store.state.competencies.length > 0">
          <item
            class="item"
            v-for="(competency, i) in this.$store.state.competencies"
            :key="i"
            :competency="competency"
            :masteryEstimates="masteryEstimates">
          </item>
        </ul>
        <div v-else text-xs-center>
          <h1>Loading CASS Competency Information...</h1>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import ActivityTile from '@/components/tiles/ActivityTile'
import LearnerApi from '@/api/learner'
import Item from '@/components/tiles/Item'
export default {
  components: {
    'item': Item
  },
  data () {
    return {
    }
  },
  computed: {
    stateMasteryEstimates () {
      return this.$store.state.userInfo.masteryEstimates
    },
    masteryEstimates () {
      let masteryEstimates = this.stateMasteryEstimates
      var mapping = {}
      for (var estIdx in masteryEstimates) {
        let key = masteryEstimates[estIdx].competencyId
        mapping[key] = masteryEstimates[estIdx].mastery
      }
      return mapping
    }
  },
  methods: {
  },
  created () {
  }
}
</script>
