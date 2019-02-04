import axios from 'axios'
export default {
  async getLearner (learnerId) {
    let result = await axios.get(`{fluent_server_here}:8999/learner-inferences/learners/` + learnerId)
    let data = result.data
    return data
  },
  async getLearnerWithHeaders (learnerId) {
    // const instance = axios.create({
    //   headers: {'Access-Control-Allow-Origin': '*',
    //     'Access-Control-Allow-Methods': 'GET,HEAD,OPTIONS,POST,PUT',
    //     'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization'}
    // })
    let result = await axios.get(`{fluent_server_here}:8999/learner-inferences/learners/` + learnerId)
    return result
  },
  async patchLearner (learnerId, data, etag) {
    let config = {
      'headers': {
        'If-Match': etag
      }
    }
    let result = await axios.patch(`{fluent_server_here}:8999/learner-inferences/learners/` + learnerId, data, config)
    return result
  },
  async getRecommendations (learnerId, type) {
    if (learnerId === '') return {}
    if (type === 'upcoming') {
      let result = await axios.get('{fluent_server_here}:8979/recommender/upcoming?learnerId=' + learnerId)
      return result.data
    } else if (type === 'focused') {
      let result = await axios.get('{fluent_server_here}:8979/recommender/recommendation?focusedCompetencies=true&learnerId=' + learnerId)
      return result.data
    }
    let result = await axios.get('{fluent_server_here}:8979/recommender/recommendation?learnerId=' + learnerId)
    return result.data
  }
}
