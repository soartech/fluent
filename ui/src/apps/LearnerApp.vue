<template>
  <v-app>
    <v-toolbar
      app
      :clipped-right="true"
      height='45'
      style="background-color: #ececea"
    >
      <router-link to="/">
        <img src="/static/img/icons/TLA_top_banner3.jpg" alt="TLA" style="height: 40px; padding-top: 5px;">
      </router-link>
      <v-spacer></v-spacer>
      <div>
        <v-toolbar-title v-text="title" class="text-lg-right display"></v-toolbar-title>
      </div>
    </v-toolbar>
  <v-navigation-drawer
      :clipped="true"
      app
      hide-overlay
      :mini-variant="mini"
      mobile-break-point=0
      :v-model="true"
      touchless
      style="z-index: 0;"
      right
      width="375"
    >
      <v-layout justify-center>
          <v-btn icon @click="toggleMiniMode">
            <v-icon style="font-size: 30px;">menu</v-icon>
          </v-btn>
      </v-layout>
      <v-list>
        <div v-for="(item, i) in items" :key="i">
          <v-tooltip left v-if="mini">
            <v-list-tile
              value="true"
              slot="activator"
              :to="item.route"
              @click="item.toggleModal ? dialog = !dialog : ''"
              replace
              >
                <v-list-tile-action>
                  <v-icon style="font-size: 30px; line-height: 23px;" v-html="item.icon"></v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                  <v-list-tile-title style="font-size: 20px; height: 23px; line-height: 23px;" v-text="item.title"></v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
            <span>{{item.title}}</span>
          </v-tooltip>
          <v-list-tile v-else
              value="true"
              slot="activator"
              :to="item.route"
              @click="item.toggleModal ? dialog = !dialog : ''"
              replace
              >
                <v-list-tile-action>
                  <v-icon style="font-size: 30px; line-height: 23px;" v-html="item.icon"></v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                  <v-list-tile-title style="font-size: 20px; height: 23px; line-height: 23px;" v-text="item.title"></v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
        </div>
      </v-list>
    </v-navigation-drawer>
    
    <v-content>
      <router-view/>
    </v-content>
      <span></span>

    <v-dialog
      v-model="dialog"
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
          Are you sure you want to sign out?  
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="logout"
            flat
          >
            Yes
          </v-btn>
          <v-btn
            color="secondary"
            flat
            @click="dialog = false"
          >
            no
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import ActivitiesApi from '@/api/activities'
import CompetenciesApi from '@/api/competencies'
import LearnerApi from '@/api/learner'
import xAPI from '@/api/sendXAPI'
export default {
  data () {
    return {
      dialog: false,
      mini: true,
      items: [
        {
          icon: 'device_hub',
          title: 'Graphical Skill Tree',
          route: '/'
        },
        {
          icon: 'library_books',
          title: 'All Recommendations',
          route: '/activities'
        },
        {
          icon: 'collections_bookmark',
          title: 'Focused Recommendations',
          route: '/activities/focused'
        },
        {
          icon: 'format_list_bulleted',
          title: 'All Activities for Selected Goal',
          route: '/activities/all'
        },
        {
          icon: 'account_box',
          title: 'Sign Out',
          toggleModal: true
        }
        
      ],
      title: 'FLUENT TLA'

    }
  },
  methods: {
    toggleMiniMode () {
      this.mini = !this.mini
    },
    async loadAll() {
      // Initializes Keycloak Single Sign-On (SSO), based on data in accompanying keycloak.json file;
        var keycloak = global.Keycloak(
          {
            'realm': 'fluent',
            'auth-server-url': '{keycloak_server_here}:8081/auth',
            'ssl-required': 'none',
            'clientId': 'fluent-ui-dashboard',
            'public-client': true,
            'confidential-port': 0
          }
        )
        console.log('Started loading operations')
        await this.$store.dispatch('loadKeycloak', keycloak)
        await this.$store.dispatch('loadCompetencies')
        await this.$store.dispatch('loadActivities')
        await this.$store.dispatch('checkGoals')
        console.log('Ended loading operations')
    },
    logout() {
      xAPI.sendLoggedOut(this.$store.state.userInfo)
      window.location = "{keycloak_server_here}:8081/auth/realms/fluent/account/sessions"
    }
  },
  computed: {
  },
  watch: {
    async $route (to, from) {
      await this.$store.dispatch('setMasteryEstimates', this.$store.state.userInfo.id)
    }
  },
  async beforeMount () {
    // Initializes Keycloak Single Sign-On (SSO), based on data in accompanying keycloak.json file;
    this.loadAll()
  }
}
</script>

<style>
</style>