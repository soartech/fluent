<template>
  <v-app>
    <v-toolbar
      app
      :clipped-left="true"
      height='150'
      style="background-color: #ececea"
    >
      <router-link to="/">
        <img src="/static/img/icons/tla_2017.png" alt="Vuetify.js" style="height: 125px;">
      </router-link>
      <v-spacer></v-spacer>
      <div>
        <v-toolbar-title v-text="title" class="text-lg-right display-3"></v-toolbar-title>
      </div>
    </v-toolbar>
  <v-navigation-drawer
      :clipped="true"
      app
      hide-overlay
      :mini-variant.sync="mini"
      mobile-break-point=0
      :v-model="true"
      touchless
      style="z-index: 0;"
    >
      <v-layout justify-center>
          <v-btn icon @click="toggleMiniMode">
            <v-icon>menu</v-icon>
          </v-btn>
      </v-layout>
      <v-list>
        <v-list-tile
          value="true"
          v-for="(item, i) in items"
          :key="i"
          :to="item.route"
          replace
          >
            <v-list-tile-action>
              <v-icon v-html="item.icon"></v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title v-text="item.title"></v-list-tile-title>
            </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    
    <v-content>
      <router-view/>
    </v-content>
        <v-footer :fixed="true" app>
      <span></span>
    </v-footer>
  </v-app>
</template>

<script>
import ActivitiesApi from '@/api/activities'
import CompetenciesApi from '@/api/competencies'
import LearnerApi from '@/api/learner'
export default {
  data () {
    return {
      mini: true,
      items: [
        {
          icon: 'assignment_turned_in',
          title: 'Placeholder Item',
          route: '/'
        }],
      title: 'FLUENT Ft. Bragg Demo'

    }
  },
  methods: {
    toggleMiniMode () {
      this.mini = !this.mini
    },
    loadActivities: async function () {
      let activities = await ActivitiesApi.getActivities()
      this.$store.commit('setActivities', activities)
    },
    loadCompetencies: async function () {
      var competencies = []
      if (localStorage.getItem('competencies')) {
        competencies = await JSON.parse(localStorage.getItem('competencies'))
      } else {
        competencies = await CompetenciesApi.getCompetencies()
        localStorage.setItem('competencies', JSON.stringify(competencies))
      }
      this.$store.commit('setCompetencies', competencies)
    }
  },
  computed: {
  },
  async created () {
    // Initializes Keycloak Single Sign-On (SSO), based on data in accompanying keycloak.json file;
    var keycloak = global.Keycloak(
      {
        'realm': 'fluent',
        'auth-server-url': 'insertIPAddr/auth',
        'ssl-required': 'none',
        'clientId': 'fluent-ui-dashboard',
        'public-client': true,
        'confidential-port': 0
      }
    )
    keycloak.init({ onLoad: 'login-required', flow: 'implicit' }).success(async function (authenticated) {
      //keycloak.idTokenParsed
      console.log('Keycloak login successful')
      this.$store.commit('setUserFromKeycloak', keycloak)

      let learnerInfo = await LearnerApi.getLearner(keycloak.idTokenParsed.sub)
      this.$store.commit('setMasteryEstimates', learnerInfo.masteryEstimates)
      // Fields available: email, family_name, given_name, name, preferred_username
    }.bind(this)).error(function (error) {
      alert('Failed to initialize authentication')
      console.log('Keycloak sign-in error')
      console.log(error)
    })
    this.loadCompetencies()
    this.loadActivities()
  }
}
</script>

<style>
</style>