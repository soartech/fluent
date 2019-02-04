<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <h2>{{ recommendedOrAll }} Activities for Goal: <span style="font-weight: normal">{{ currentGoalName }}</span></h2>
      </v-flex>
    </v-layout>
    <div v-if="recommendationsReady && activities.length > 0 && !recommendationsUpdating">
      <v-layout row wrap>
        <v-flex xs1>
          <v-btn class="arrowBtn" style="height: 100%" @click="decreaseOffset()" :disabled="!canGoBack"><v-icon v-html="'arrow_back'"></v-icon></v-btn>
        </v-flex>
        <v-flex xs10>
          <v-container grid-list-xl>
            <v-layout row wrap justify-center>
              <activity-tile
              v-for="(activity, i) in activities" :key="i+offset"
              v-bind:selected="selectedIdx == i+offset"
              :identifier="getActivityId(activity)"
              :imageSrc="activity.image"
              :title="activity.name"
              :description="activity.description"
              :index="i+offset"
              :tokens="tokenValue(getActivityId(activity))"
              :launched="getActivityLaunched(activity.identifier)"
              :setIdx="setIdx"/>
            </v-layout>
          </v-container>
        </v-flex>
        <v-flex xs1 text-xs-right>
          <v-btn class="arrowBtn" style="height: 100%" @click="increaseOffset()" :disabled="!canGoForward"><v-icon v-html="'arrow_forward'"></v-icon></v-btn>
        </v-flex>
      </v-layout>
      <v-layout row>
        <v-spacer/>
        <v-flex xs6 sm7 md10 text-xs-center style="padding-top: 15px;">
          <h3 style="font-weight: normal;"> Showing {{ 1+this.offset }} - {{ shownOffset }} of {{ this.allActivities.length }}</h3>
        </v-flex>
        <v-spacer/>
      </v-layout>
      <v-layout row style="padding-top: 20px;">
        <v-flex xs12>
          <activity-info
          :activity="currentActivity"
          :tags="currentActivityTags"
          :setActivityLaunched="setActivityLaunched"
          />
        </v-flex>
      </v-layout>
      <v-layout v-if="this.showSelfReport" row style="padding-top: 20px;">
        <v-flex xs12>
          <self-report
          :updateSubmitted="updateReportSubmitted"
          :activityId="currentActivity.identifier"/>
        </v-flex>
      </v-layout>
    </div>
    <div v-else-if="recommendationsReady && activities.length == 0 && recommendationsEmpty">
      <v-layout row>
        <v-spacer/>
        <v-flex xs11 sm6 md5 lg3>
          <info-card
          :infoText="'No Recommendations. Please choose a new goal.'"/>
        </v-flex>
        <v-spacer/>
      </v-layout>
    </div>
    <div v-else>
      <v-layout row>
        <v-spacer/>
        <v-flex xs11 sm6 md5 lg3>
          <loading-tile
          :loadingText="loadingText"/>
        </v-flex>
        <v-spacer/>
      </v-layout>
    </div>
  </v-container>
</template>

<script>
import ActivityTile from '@/components/tiles/ActivityTile'
import ActivityInfo from '@/components/tiles/ActivityInfo'
import LoadingTile from '@/components/tiles/LoadingTile'
import SelfReport from '@/components/tiles/SelfReport'
import InfoCard from '@/components/tiles/InfoCard'
import ActivitiesApi from '@/api/activities'
import LearnerApi from '@/api/learner'
import xAPI from '@/api/sendXAPI'
export default {
  data () {
    return {
      selectedIdx: 0,
      itemsToShow: 6,
      offset: 0,
      recommendations: {},
      selfReportVisible: false,
      launchedActivities: [],
      recommendationsUpdating: false,
      mostRecentRecommendationTime: null,
      recommendationsReadyOld: false,
      collaborativeReasons: [
        'HighestRatedActivities',
        'PopularActivities',
        'MoreFromAuthorActivities',
        'MoreFromProviderActivities',
        'MoreVideosActivities'
      ],
      recommendationsReadyOld: false,
      recommendationsEmpty: false
    }
  },
  components: {
    'activity-tile': ActivityTile,
    'activity-info': ActivityInfo,
    'self-report': SelfReport,
    'loading-tile': LoadingTile,
    'info-card': InfoCard
  },
  watch: {
    activityTags (tags) {
      var activityList = []
      for (var activityId in tags) {
        var priority = 0
        var reasons = []
        for (var tagIdx in tags[activityId]) {
          priority += tags[activityId][tagIdx].paradata.priority
          reasons.push(tags[activityId][tagIdx].name)
        }
        priority = Math.round(priority*100)
        activityList.push({
          activityId: activityId,
          priority: priority,
          recommendationReasons: reasons
        })
      }
      activityList = activityList.sort(function (a, b) {
        if (a.priority < b.priority) {
          return 1
        } else if (a.priority > b.priority) {
          return -1
        } else {
          return 0
        }
      })

      if (activityList.length > 0) {
        console.log(this.userInfo)
        xAPI.sendRecommendationOrdering(this.userInfo, activityList)
      }
    }
  },
  computed: {
    showAllActivities() {
      if (this.$route.path.endsWith('/all')) {
        return true;
      }
      return false;
    },
    showFocusedActivities () {
      if (this.$route.path.endsWith('/focused')) {
        return true
      } else {
        return false
      }
    },
    filterOutCollaborativeReasons () {
      if (localStorage.getItem('collaborativeFiltering') !== null) {
        return localStorage.getItem('collaborativeFiltering') == 'false'
      } else {
        return true
      }
    },
    loadingText() {
      if (this.$route.path.endsWith("/all")) {
        return "Loading All Activities"
      } else {
        return "Loading Recommended Activities"
      }
    },
    shownOffset() { 
      if (this.itemsToShow+this.offset < this.allActivities.length) {
        return this.itemsToShow+this.offset
      } else {
        return this.allActivities.length
      }
    },
    recommendedOrAll() {
      if (this.showAllActivities) return "All"
      else if (this.showFocusedActivities) return "Recommended (Focused)"
      else return "Recommended"
    },
    learnerGoal () {
      return this.$store.state.userInfo.goal
    },
    userInfo () {
      return this.$store.state.userInfo
    },
    allActivities () {
      return this.sortActivities(this.filterActivities(this.$store.state.activities))
    },
    activities () {
      return this.allActivities.slice(0+this.offset, this.itemsToShow+this.offset)
    },
    canGoForward() {
      return this.offset < (this.allActivities.length - this.itemsToShow)
    },
    canGoBack() {
      return this.offset > 0
    },
    currentActivity() {
      if (this.allActivities.length > 0) {
        return this.allActivities[this.selectedIdx]
      } else {
        return null
      }
    },
    showSelfReport() {
      return (this.selfReportVisible)
    },
    currentActivityTags () {
      if (this.currentActivity !== null) {
        if (this.currentActivity.identifier in this.activityTags) {
          return this.activityTags[this.currentActivity.identifier]
        }
      } else {
        return []
      }
    },
    currentGoal() {
      return this.$store.state.competencyMappings[this.learnerGoal]
    },
    currentGoalName() {
      if (this.currentGoal) {
        return this.currentGoal.name
      } else {
        return 'N/A'
      }
    },
    activityTags () {
      var activityTags = {}
      let recommendationRows = this.recommendations.recommendations
      for (var idx in recommendationRows) {
        let row = recommendationRows[idx]
        for (var activityIdx in recommendationRows[idx].activities) {
          var tag = {
            name: row.name,
            strategy: row.strategy,
            params: row.params,
            paradata: recommendationRows[idx].activities[activityIdx]
          }
          if (this.filterOutCollaborativeReasons && this.collaborativeReasons.indexOf(tag.strategy) >= 0) {
            continue
          }
          var activityId = recommendationRows[idx].activities[activityIdx].activityId
          if (!(activityId in activityTags)) {
            activityTags[activityId] = []
          }
          activityTags[activityId].push(tag)
          this.$store.commit('setParadata', [activityId, recommendationRows[idx].activities[activityIdx]])
        }
      }
      return activityTags
    },
    async recommendationsReady () {
      var recType = "recommendations"
      if (this.showAllActivities) {
        recType = "upcoming"
      } else if (this.showFocusedActivities) {
        recType = "focused"
      }
      this.recommendationsUpdating = true
      var currentRequestTime = new Date()
      this.mostRecentRecommendationTime = currentRequestTime
      let recommendations = await this.$store.dispatch('getRecommendations', recType)

      // Tries to mitigate if we have an older request (between switching pages)
      if (this.mostRecentRecommendationTime == currentRequestTime) {
        this.recommendations = recommendations

        // Send xAPI
        xAPI.sendRecommendations(this.$store.state.userInfo, recommendations)
        this.recommendationsReadyOld = 'recommendations' in recommendations
        if (this.recommendationsReadyOld) {
          let recommendationsList = recommendations['recommendations']
          if (recommendationsList.length == 0) {
            this.recommendationsEmpty = true
          } else {
            this.recommendationsEmpty = false
          }
        }
      }
      this.recommendationsUpdating = false
      return this.recommendationsReadyOld
    }
  },
  methods: {
    tokenValue (activityId) {
      if (activityId !== null && this.activityTags[activityId] !== null) return this.activityTags[activityId][0].paradata.tokens
      return 1
    },
    setIdx (index) {
      // Do nothing if it's the same index
      if(this.selectedIdx === index)
        return

      this.selectedIdx = index
      this.setSelfReportVisible(false)
    },
    getActivityId(activity) {
      if (activity != null && 'identifier' in activity) {
        return activity['identifier']
      }
      return null
    },
    increaseOffset() {
      this.offset = Math.min(this.offset + this.itemsToShow, this.allActivities.length - this.itemsToShow)
    },
    decreaseOffset() {
        this.offset = Math.max(this.offset - this.itemsToShow, 0)
    },
    setSelfReportVisible(value) {
      this.selfReportVisible = value
    },
    updateReportSubmitted(value) {
      this.setSelfReportVisible(!value)
    },
    updateStoredActivityMetadata() {

    },
    filterActivities(activityList) {
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
      if (this.showAllActivities) {
        activityList.sort(this.sortAlphabetically)
      } else {
        activityList.sort(this.sortByPriority)
      }
      return activityList
    },
    calculatePriority(activity) {
      var priority = 0
      for (var tagIdx in this.activityTags[activity.identifier]) {
        var paradata = this.activityTags[activity.identifier][tagIdx].paradata
        priority += parseFloat(paradata.priority)
      }
      return priority
    },
    sortByPriority(a, b) {
      let aPriority = this.calculatePriority(a)
      let bPriority = this.calculatePriority(b)
      if (aPriority > bPriority) {
        return -1
      } else if (aPriority < bPriority) {
        return 1
      } else {
        return 0
      }
    },
    sortAlphabetically(a, b) {
      if(a.name.trim() < b.name.trim()) return -1;
      if(a.name.trim() > b.name.trim()) return 1;
      return 0
    },
    setActivityLaunched(activityId) {
      if (this.launchedActivities.indexOf(activityId) < 0) {
        this.launchedActivities.push(activityId)
      }

      // Show the self-report
      this.setSelfReportVisible(true)
    },
    getActivityLaunched(activityId) {
      if (this.launchedActivities.indexOf(activityId) >= 0) {
        return true
      }
      return false
    }
  },
  async created () {
  }
}
</script>

<style>
  .arrowBtn .btn__content {
    padding: 0;
    height: 100%
  }

  .arrowBtn {
    min-width: 0 !important;
    width: 75%;
    height: 100%;
  }
</style>
