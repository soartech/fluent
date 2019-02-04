<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <h2>Frameworks</h2>
      </v-flex>
    </v-layout>
    <v-layout row  v-if="this.$store.state.competencies.length > 0">
      <v-flex xs12>
        <ul id="competencyList">
          <item
            class="item"
            v-for="(competency, i) in this.$store.state.competencies"
            :key="i"
            :competency="competency"
            :masteryProbabilities="masteryProbabilities"
            :headNode="true">
          </item>
        </ul>
      </v-flex>
    </v-layout>
    <v-layout v-else row>
      <v-spacer/>
      <v-flex xs11 sm6 md5 lg3>
        <loading-tile
        :loadingText="'Loading Competency Structure'"/>
      </v-flex>
      <v-spacer/>
    </v-layout>
  </v-container>
</template>

<script>
import LoadingTile from '@/components/tiles/LoadingTile'
import LearnerApi from '@/api/learner'
import Item from '@/components/tiles/Item'
export default {
  components: {
    'item': Item,
    'loading-tile': LoadingTile
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
    },
    stateMasteryProbabilities () {
      return this.$store.state.userInfo.masteryProbabilities
    },
    masteryProbabilities () {
      let masteryProbabilities = this.stateMasteryProbabilities
      if (this.stateMasteryProbabilities == null) return {}
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
  methods: {
  },
  created () {
  }
}
</script>
