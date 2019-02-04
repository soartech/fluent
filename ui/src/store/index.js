import Vue from 'vue'
import Vuex from 'vuex'
import LearnerApi from '@/api/learner'
import ActivitiesApi from '@/api/activities'
import CompetenciesApi from '@/api/competencies'
import xAPI from '@/api/sendXAPI'
Vue.use(Vuex)

const store = new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  state: {
    currentInterval: undefined,
    userInfo: {
      username: '',
      id: '',
      firstName: '',
      lastName: '',
      goal: '',
      masteryEstimates: [],
      masteryProbabilities: []
    },
    activities: [],
    competencies: [],
    competencyMappings: {},
    relations: []
  },
  mutations: {
    setUserInfo (state, info) {
      state.userInfo = info
    },
    setUserFromKeycloak (state, keycloak) {
      state.userInfo.username = keycloak.idTokenParsed.preferred_username
      state.userInfo.id = keycloak.idTokenParsed.sub
      state.userInfo.firstName = keycloak.idTokenParsed.given_name
      state.userInfo.lastName = keycloak.idTokenParsed.family_name

      // Send logged in xAPI
      xAPI.sendLoggedIn(state.userInfo)
    },
    setCurrentInterval (state, interval) {
      if (state.currentInterval) {
        clearInterval(state.currentInterval)
      }
      state.currentInterval = interval
    },
    setActivities (state, activities) {
      var activitiesDict = {}
      for (var idx in activities) {
        activitiesDict[activities[idx].identifier] = activities[idx]
      }
      state.activities = activitiesDict
    },
    setCompetencies (state, competencies) {
      state.competencies = competencies.objectList
      state.competencyMappings = competencies.idMap
      state.relations = competencies.relations
    },
    setMasteryEstimates (state, masteryEstimates) {
      state.userInfo.masteryEstimates = masteryEstimates
    },
    setMasteryProbabilities (state, masteryProbabilities) {
      state.userInfo.masteryProbabilities = masteryProbabilities
    },
    setLearnerGoal (state, goalId) {
      state.userInfo.goal = goalId
    },
    setParadata (state, list) {
      let activityId = list[0]
      let paradata = list[1]
      if (paradata != null) {
        if (activityId in state.activities) {
          if ('popularityRating' in paradata) {
            state.activities[activityId].popularityRating = paradata.popularityRating
          }
          if ('attemptRate' in paradata) {
            state.activities[activityId].attemptRate = paradata.attemptRate
          }
        }
      }
    }
  },
  actions: {
    async patchLearnerGoal ({dispatch, rootState, state}, goalId) {
      let payload = {
        'goals': [{
          '@context': 'tla-declarations.jsonld',
          '@type': 'Goal',
          'competencyId': goalId
        }]
      }
      console.log(rootState)
      console.log(state.userInfo.id)
      // Not working right now - try again later.
      let getResult = await LearnerApi.getLearnerWithHeaders(state.userInfo.id)
      console.log(getResult)
      let etag = getResult.headers['etag']
      let result = await LearnerApi.patchLearner(state.userInfo.id, payload, etag)

      // Send xAPI
      xAPI.sendGoalSet(state.userInfo, goalId)

      return result
    },
    async getRecommendations ({dispatch, rootState, state}, recType) {
      let result = await LearnerApi.getRecommendations(state.userInfo.id, recType)
      return result
    },
    async loadKeycloak ({ commit, dispatch }, keycloak) {
      console.log('Starting keycloak login...')
      await keycloak.init({ onLoad: 'login-required', flow: 'implicit' }).success(async function (authenticated) {
        // keycloak.idTokenParsed
        console.log('Keycloak login successful')
        commit('setUserFromKeycloak', keycloak)
        await dispatch('setMasteryEstimates', keycloak.idTokenParsed.sub)
        // Fields available: email, family_name, given_name, name, preferred_username
      }).error(function (error) {
        alert('Failed to initialize authentication')
        console.log('Keycloak sign-in error')
        console.log(error)
      })
    },
    async setMasteryEstimates ({ commit, dispatch }, learnerId) {
      let learnerInfo = await LearnerApi.getLearner(learnerId)
      commit('setMasteryEstimates', learnerInfo.masteryEstimates)
      commit('setMasteryProbabilities', learnerInfo.masteryProbabilities)
      if (learnerInfo.goals.length > 0) commit('setLearnerGoal', learnerInfo.goals[0].competencyId)
    },
    async loadActivities ({commit}) {
      console.log('Loading activities...')
      let activities = await ActivitiesApi.getActivities()
      commit('setActivities', activities)
      console.log('Done loading activities.')
    },
    async loadCompetencies ({commit}) {
      var competencies = []
      console.log('Loading competencies...')
      if (localStorage.getItem('competencies')) {
        competencies = await JSON.parse(localStorage.getItem('competencies'))
      } else {
        competencies = await CompetenciesApi.getCompetencies()
        localStorage.setItem('competencies', JSON.stringify(competencies))
      }
      commit('setCompetencies', competencies)
      console.log('Done loading competencies.')
    },
    async checkGoals ({commit, state, dispatch}) {
      console.log('Checking Goals')
      var goal = null
      if (state.userInfo.goal !== '') {
        console.log('Goal found!')
        return
      }
      for (var compIdx in state.competencies) {
        let badge = state.competencies[compIdx]
        var found = false
        for (var estIdx in state.userInfo.masteryEstimates) {
          var masteryEstimate = state.userInfo.masteryEstimates[estIdx]
          if (masteryEstimate.competencyId === badge['@id']) {
            found = true
            if (masteryEstimate.mastery !== 'expert') {
              goal = badge['@id']
              break
            }
          }
        }
        if (!found) {
          goal = badge['@id']
          break
        }
      }

      if (goal !== null) {
        console.log('No goal for learner found, patching goal instead')
        await dispatch('patchLearnerGoal', goal)
        commit('setLearnerGoal', goal)
      } else {
        console.log('No valid goal found for learner')
      }
    }
  },
  getters: {
    userInfo: state => state.userInfo
  }
})

export default store
