<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <h2>Administrative Options</h2>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-spacer/>
      <v-flex xs10 sm9 md8 lg7 xl6>
        <v-card>
          <v-container fluid>
            <v-layout style="padding-bottom: 10px;" row>
              <v-flex xs12>
                <h3> Options </h3>
              </v-flex>
            </v-layout>
            <v-divider/>
            <v-layout style="padding-top: 10px; padding-bottom: 10px;" row wrap>
              <v-flex xs12 md10>
                <h3 style="padding-top: 10px; font-weight: normal;">Clear cached competency information (will reload page)</h3>
              </v-flex>
              <v-flex xs6 md2>
                <v-btn @click="clearStorage()">Clear</v-btn>
              </v-flex>
            </v-layout>
            <v-divider/>
            <v-layout style="padding-top: 10px;" row wrap>
              <v-flex xs12 md10>
                <h3 style="padding-top: 10px; font-weight: normal;">Enable/Disable Collaborative Filtering: </h3>
              </v-flex>
              <v-flex xs6 md2>
                <v-btn @click="setCollaborativeFiltering()">{{ collaborativeFiltering ? 'Disable' : 'Enable'}}</v-btn>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>
      <v-spacer/>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  methods: {
    clearStorage () {
      localStorage.clear()
      sessionStorage.clear()
      window.location = '/'
    },
    setCollaborativeFiltering () {
      this.collaborativeFiltering = !this.collaborativeFiltering
      localStorage.setItem('collaborativeFiltering', this.collaborativeFiltering)
    },
    initCollaborativeFiltering () {
      if (localStorage.getItem('collaborativeFiltering') !== null) {
        this.collaborativeFiltering = localStorage.getItem('collaborativeFiltering') == 'true'
      } else {
        this.collaborativeFiltering = true
      }
    }
  },
  data () {
    return {
      collaborativeFiltering: true
    }
  },
  created () {
    this.initCollaborativeFiltering()
  }
}
</script>
