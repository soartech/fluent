import axios from 'axios'
export default {
  async getActivities () {
    let result = await axios.get(`insertIPAddr/activity-index/activities`)
    let data = result.data
    return data
  }
}
