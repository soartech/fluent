import axios from 'axios'
export default {
  async getLearner (learnerId) {
    let result = await axios.get(`insertIPAddr/learner-inferences/learners/` + learnerId)
    let data = result.data
    return data
  },
  async getLearnerWithHeaders (learnerId) {
    // const instance = axios.create({
    //   headers: {'Access-Control-Allow-Origin': '*',
    //     'Access-Control-Allow-Methods': 'GET,HEAD,OPTIONS,POST,PUT',
    //     'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization'}
    // })
    let result = await axios.get(`insertIPAddr/learner-inferences/learners/` + learnerId)
    return result
  },
  async patchLearner (learnerId, data) {
    let result = await axios.patch(`insertIPAddr/learner-inferences/learners/` + learnerId, data)
    return result
  },
  async getRecommendations (learnerId) {
    let result = await axios.get('insertIPAddr/recommender/recommendation?learnerId=' + learnerId)
    return result.data
  }
}
