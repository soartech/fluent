<template>
  <router-view/>
</template>

<script>
export default {
  beforeCreate () {
    // let userInfo = {}
    // Object.keys(this.$store.state.userInfo).forEach(k => {
    //   userInfo[k] = this.$cookie.get(k)
    // })
    // this.$store.commit('setUserInfo', userInfo)
  }
}
</script>