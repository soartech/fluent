import Vue from 'vue'
import Vuex from 'vuex'
import LearnerApi from '@/api/learner'
Vue.use(Vuex)

const store = new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  state: {
    currentInterval: undefined,
    userInfo: {
      username: '',
      id: '',
      masteryEstimates: []
    },
    activities: [],
    competencies: []
  },
  mutations: {
    setUserInfo (state, info) {
      state.userInfo = info
    },
    setUserFromKeycloak (state, keycloak) {
      state.userInfo.username = keycloak.idTokenParsed.preferred_username
      state.userInfo.id = keycloak.idTokenParsed.sub
    },
    setCurrentInterval (state, interval) {
      if (state.currentInterval) {
        clearInterval(state.currentInterval)
      }
      state.currentInterval = interval
    },
    setActivities (state, activities) {
      state.activities = activities
    },
    setCompetencies (state, competencies) {
      state.competencies = competencies
    },
    setMasteryEstimates (state, masteryEstimates) {
      state.userInfo.masteryEstimates = masteryEstimates
    }
  },
  actions: {
    async patchLearnerGoal ({dispatch, rootState, state}, goalId) {
      let payload = {
        'goals': [{
          '@context': 'tla-declarations.jsonld',
          '@type': 'Goal',
          'competencyId': 'insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/8f97e65b-1d2e-4973-9ddc-47fed9dced41'
        }]
      }
      console.log(rootState)
      console.log(state.userInfo.id)
      // Not working right now - try again later.
      let getResult = await LearnerApi.getLearnerWithHeaders(state.userInfo.id)
      console.log(getResult)
      let result = await LearnerApi.patchLearner(state.userInfo.id, payload)
      return result
    },
    async getRecommendations ({dispatch, rootState, state}, goalId) {
      let result = await LearnerApi.getRecommendations(state.userInfo.id)
      return result
    }
  },
  getters: {
    getUserInfo: state => state.userInfo.id
  }
})

export default store
