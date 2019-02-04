<template>
  <v-card>
    <v-container fluid>
      <v-layout row wrap>
        <v-flex xs4>
          <h2>How did you feel after that activity?</h2>
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex xs6 sm4 md3 lg2 xl1 v-for="rating in moods" :key="rating.text">
          <h3 @click="selectedMood = rating.text" :class="emotionRatingClasses(rating.text)" style="margin: 3px; font-weight: normal;"><span>{{ rating.icon }} {{ rating.displayName }}</span></h3>
        </v-flex>
      </v-layout>
      <v-layout row>
        <v-flex xs4>
          <h2>Please rate the activity:</h2>
        </v-flex>
        <v-flex xs8>
          <h2><star-rating :setterValue="value" :setterFunc="setRating"/></h2>
        </v-flex>
      </v-layout>
      <v-layout row>
        <v-spacer/>
        <v-flex text-xs-right>
          <v-btn @click="submitSelfReport()">Submit</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
import StarRating from '@/components/tiles/StarRating'
import axios from 'axios'
export default {
  data () {
    return {
      moods: [
        {
          text: 'frustrating',
          displayName: 'Frustrated',
          icon: '😤'
        },
        {
          text: 'confusing',
          displayName: 'Confused',
          icon: '🤨'
        },
        {
          text: 'boring',
          displayName: 'Bored',
          icon: '😐'
        },
        {
          text: 'flow',
          displayName: 'Focused',
          icon: '🤔'
        },
        {
          text: 'eureka',
          displayName: 'Eureka',
          icon: '🤩'
        }
      ],
      value: 0,
      selectedMood: null
    }
  },
  props: {
    updateSubmitted: Function,
    activityId: String
  },
  methods: {
    log: function (msg) {
      console.log(msg)
    },
    setRating: function (value) {
      this.value = value
    },
    submitSelfReport() {
      // Build the report Object
      let dateString = new Date().toISOString()
      let url = "{fluent_server_here}:8778/rui-support/activity-responses"
      let responseObject = {
        'emotionRating': this.selectedMood,
        'popularityRating': this.value,
        'learnerKeycloakId': this.$store.state.userInfo.id,
        'timestamp': dateString
      }

      // Send the POST
      axios.post(url, responseObject);

      // makes the self report go away
      this.updateSubmitted(true)
    },
    emotionRatingClasses: function (ratingText) {
      var classString = 'pa-1 emotionIcon'
      if (ratingText === this.selectedMood) {
        classString += ' selected'
      }
      return classString
    }
  },
  components: {
    'star-rating': StarRating
  }
}
</script>

<style>
  .emotionIcon {
    cursor: pointer
  }
  .selected {
    background-color: lightgray;
  }
</style>
