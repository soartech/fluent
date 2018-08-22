<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <h1>Activities for All ELOs</h1>
      </v-flex>
    </v-layout>
    <div v-if="activities.length > 0">
      <v-layout row v-for="activity in activities" :key="activity.title">
        <activity-tile
        :title="activity.name"
        :description="activity.description"
        :imageSrc="activity.image"
        :launchUrl="activity.url"/>
      </v-layout>
    </div>
    <div v-else>
      <v-layout row text-xs-center>
        <v-flex>
          <h1 id="loadingText">Loading...</h1>
        </v-flex>
      </v-layout>
    </div>
  </v-container>
</template>

<script>
import ActivityTile from '@/components/tiles/ActivityTile'
import ActivitiesApi from '@/api/activities'
import LearnerApi from '@/api/learner'
export default {
  data () {
    return {
      activityTags: {}
    }
  },
  components: {
    'activityTile': ActivityTile
  },
  computed: {
    competencyUrl () {
      return 'insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/'+this.$route.params.id
    },
    activities () {
      return this.sortActivities(this.filterActivities(this.$store.state.activities))
    }
  },
  methods: {
    handleRecommendations(recommendationRows) {
      this.activityTags = {}
      for (var idx in recommendationRows) {
        let tag = recommendationRows[idx].name
        console.log(tag)
        for (var activityIdx in recommendationRows[idx].activities) {
          let activityId = recommendationRows[idx].activities[activityIdx].activityId
          if (!(activityId in this.activityTags)) {
            this.activityTags[activityId] = []
          }
          this.activityTags[activityId].push(tag)
        }
      }
    },
    filterActivities(activityList) {
      console.log(activityList)
      var activityReturnList = []
      for (var activityIdx in activityList) {
        let identifier = activityList[activityIdx].identifier
        if (identifier in this.activityTags) {
          activityReturnList.push(activityList[activityIdx])
        }
      }
      return activityReturnList
    },
    sortActivities(activityList) {
      return activityList
    }
  },
  async created () {
    if (!this.$route.params.id) {
      this.$router.replace('/')
    }

    // not working for now - let result = await this.$store.dispatch('patchLearnerGoal', 'testId')

    //get recommendations
    let recommendations = await this.$store.dispatch('getRecommendations')
    console.log(recommendations)
    this.handleRecommendations(recommendations.recommendations)
  }
}
</script>
