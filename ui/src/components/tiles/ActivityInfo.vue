<template>
  <v-card>
    <v-container grid-list-md fluid>
      <v-layout row>
        <v-flex xs6>
          <h2>{{ activityName }}</h2>
        </v-flex>
        <v-spacer/>
        <v-flex xs6 style="text-align: right;">
          <h2> {{activityPopularityRating}} </h2>
        </v-flex>
      </v-layout>
      <v-layout row>
        <v-flex xs12>
          <h3 style="font-weight: normal; font-style: italic;">{{ activityDescription }}</h3>
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex xs12 sm6>
          <div v-for="(info, i) in column1Info" :key="i">
            <h3>{{ info.display }}: <span style="font-weight: normal">{{ info.text }}</span></h3>
          </div>
        </v-flex>
        <v-flex xs12 sm6>
          <h3 v-if="!showAllActivities">Recommendation Reason(s): <span style="font-weight: normal;"> <span v-if="allActivitiesForCompetency.length > 0">Supports Goal for {{ allActivitiesForCompetency.length }} Competencies <span v-if="showExpandedForCompetencyAlignments"> ({{ allActivitiesForCompetency.join(', ') }})</span> <span style="cursor: pointer; font-weight: bold;" @click="showHide()">({{showHideText}})</span></span><span v-if="activityRecommendationReasons !== 'N/A' || allActivitiesForCompetency.length == 0">, {{ activityRecommendationReasons }}</span></span> </h3>
          <div v-for="(info2, j) in column2Info" :key="j">
            <h3>{{ info2.display }}: <span style="font-weight: normal">{{ info2.text }}</span></h3>
          </div>
        </v-flex>
      </v-layout>
      <v-layout row text-xs-right>
        <v-flex>
          <v-btn @click="launchActivity()">Launch Activity</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
    <v-dialog
      v-model="peblDialog"
      width="500"
    >
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          Warning
        </v-card-title>

        <v-card-text>
          No devices found for PeBL activity.
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="peblDialog = false"
          >
            Okay
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'
import xAPI from '@/api/sendXAPI'
export default {
  props: {
    activity: Object,
    tags: Array,
    setActivityLaunched: Function
  },
  methods: {
    showHide () {
      this.showExpandedForCompetencyAlignments = !this.showExpandedForCompetencyAlignments
      if (this.showHideText === '+') this.showHideText = '-'
      else if (this.showHideText === '-') this.showHideText = '+'
    },
    launchActivity() {
      let launchURL = this.activity.url

      // Set activity launched
      this.setActivityLaunched(this.activity.identifier)

      // Special handler for PeBL activities
      if(launchURL.startsWith("pebl://"))
        this.launchExternalActivity(launchURL);
      else {
        window.open(launchURL, '_blank')
        xAPI.sendLaunched(this.$store.state.userInfo, this.activity)
      }

    },
    async launchExternalActivity() {
      // Grab the user info from store.state.userInfo
      let userInfo = this.$store.state.userInfo

      // Get the user's list of devices
      let devices = await this.getDevices(userInfo)

      // If there are devices available, prompt then launch on one
      if(devices !== undefined && devices.length > 0) {
        // TODO: prompt which device to launch on
        //       for now, just launch on first device
        let index = 0

        this.launchOnDevice(userInfo, devices[index].id)
      }
    },
    async getDevices(userInfo) {
      let devices = undefined
      await axios.get(`{keycloak_server_here}:8081/application-launcher/rest/device/unused/` + userInfo.username).then(response => {
        // returning the data here allows the caller to get it through another .then(...)
        devices = response.data

        // Handle if there are no user devices
        if(devices.length === 0) {
          // TODO: Make a more User friendly error
          console.log("No devices.")
          this.peblDialog = true;
        }
      })
      return devices
    },
    async launchOnDevice(userInfo, deviceId) {
      // Create the POST object
      let currentTime = Math.floor(Date.now() / 1000)
      let postObj = {
        "userId": userInfo.id,
        "deviceId": deviceId,
        "activityId": this.activity.identifier,
        "type": this.activity.url,
        "parameter": this.activity.url,
        "description": this.activity.description,
        "startTime": currentTime,
        "expireTime": currentTime,
        "creator": {
          "id": userInfo.username,
          "firstName": userInfo.firstName,
          "lastName": userInfo.lastName
        }
      }

      // Send it
      let response = await axios.post(`{keycloak_server_here}:8081/application-launcher/rest/launch/unused/`+userInfo.username+"/"+deviceId, postObj)
    },
    getAlignmentTargetUrlList (alignments, alignmentString) {
      let urlList = []
      for (var alignmentIdx in alignments) {
        let alignment = alignments[alignmentIdx]
        if (alignment.additionalType === alignmentString) {
          urlList.push(alignment.targetUrl)
        }
      }
      return urlList
    },
    getAlignmentTargetUrl (alignments, alignmentString) {
      for (var alignmentIdx in alignments) {
        let alignment = alignments[alignmentIdx]
        if (alignment.additionalType === alignmentString) {
          return alignment.targetUrl
        }
      }
      return null
    },
    getAlignedCompetency (targetUrl) {
      if (targetUrl in this.competencies) {
        return this.competencies[targetUrl]
      }
    },
    getStarVisual (rating) {
      var starString = ''
      for (var i=0; i<5; i++) {
        if (i < rating) {
          starString += '★'
        } else {
          starString += '☆'
        }
      }
      return starString
    }
  },
  computed: {
    showAllActivities() {
      if (this.$route.path.endsWith("/all")) {
        return true;
      }
      return false;
    },
    competencies () {
      return this.$store.state.competencyMappings
    },
    activityName () {
      if (this.activity !== null) {
        return this.activity.name
      } else {
        return 'N/A'
      }
    },
    activityDescription () {
      if (this.activity !== null) {
        return this.activity.description
      } else {
        return 'N/A'
      }
    },
    activityMedia () {
      if (this.activity !== null) {
        return this.activity.learningResourceType
      } else {
        return 'N/A'
      }
    },
    activityTLOAlignment () {
      if (this.activity !== null) {
        let alignmentUrl = this.getAlignmentTargetUrl(this.activity.educationalAlignment, 'TLOAlignment')
        if (alignmentUrl !== null) {
          let competency = this.getAlignedCompetency(alignmentUrl)
          return competency.name
        }
        return 'N/A'
      } else {
        return 'N/A'
      }
    },
    activityELOAlignment () {
      if (this.activity !== null) {
        let alignmentUrl = this.getAlignmentTargetUrl(this.activity.educationalAlignment, 'ELOAlignment')
        if (alignmentUrl !== null) {
          let competency = this.getAlignedCompetency(alignmentUrl)
          return competency.name
        }
        return 'N/A'
      } else {
        return 'N/A'
      }
    },
    activityELOAlignmentSet () {
      let eloSet = new Set()
      if (this.activity !== null && this.activity.educationalAlignment !== null) {
        let alignmentUrlList = this.getAlignmentTargetUrlList(this.activity.educationalAlignment, 'ELOAlignment')
        for(var competency in alignmentUrlList) {
          let compName = this.getAlignedCompetency(alignmentUrlList[competency]).name
          eloSet.add(compName)
        }
      }

      if(eloSet.length === 0)
        return null
      else
        return eloSet
    },
    activityRecommendationReasons () {
      var tagNames = []
      for (var tagIdx in this.tags) {
        var tagObj = this.tags[tagIdx]
        if (tagNames.indexOf(this.tags[tagIdx].name) < 0 && tagObj.strategy !== 'AllActivitiesForCompetency') {
          tagNames.push(this.tags[tagIdx].name)
        }
      }
      if (tagNames.length == 0) return "N/A"
      return tagNames.join(', ')
    },
    allActivitiesForCompetency () {
      var tagInfo = []
      for (var tagIdx in this.tags) {
        var tagObj = this.tags[tagIdx]
        if (tagObj.strategy === 'AllActivitiesForCompetency' && tagObj.params != null && tagObj.params.competency != null && tagInfo.indexOf(tagObj.params.competency) < 0) {
          tagInfo.push(tagObj.params.competency)
        }
      }
      return tagInfo
    },
    activityPriority () {
      var priority = 0
      for (var tagIdx in this.tags) {
        priority += this.tags[tagIdx].paradata.priority
      }
      return Math.round(priority*100)
    },
    activityPopularityRating () {
      if (this.activity !== null) {
        return this.activity.popularityRating ? this.getStarVisual(this.activity.popularityRating) : this.getStarVisual(0)
      } else {
        return 'N/A'
      }
    },
    column1Info () {
      let eloArr = Array.from(this.activityELOAlignmentSet)

      // Limit to 5 elements & append a "..."
      let eloStr = eloArr.slice(0,5).join(", ")
      if (eloArr.length > 5)
        eloStr += "..."

      return [
        {
          display: 'Media',
          text: this.activityMedia
        },
        {
          display: 'Competencies',
          text: eloStr
        }
      ]
    },
    column2Info () {
      if (!this.showAllActivities) {
        return [
          {
            display: 'Match Level',
            text: this.activityPriority
          }
        ]
      }
      return [];
    }
  },
  data () {
    return {
      peblDialog: false,
      showExpandedForCompetencyAlignments: false,
      showHideText: '+'
    }
  }
}
</script>
