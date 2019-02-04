<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12 sm8>
        <span @click="toggle" :class="{bold: isFolder}" style="font-size: 18px;"><span v-if="isFolder">{{ open ? '&#9660;' : '&#9658;' }}</span> <img v-if="headNode" style="height: 15px;" src="static/img/icons/gold-police-badge-icon-9.png"/>{{ competency.name }} <span>({{ mastery }})</span>
        </span>
      </v-flex>
      <v-flex xs12 sm4 text-xs-right>
        <v-btn color="green" v-if="userGoal === competency['@id']">Selected</v-btn>
        <v-btn v-else @click="setGoal()">Set Goal</v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  props: {
    competency: Object,
    toggle: Function,
    open: Boolean,
    mastery: String,
    headNode: Boolean
  },
  computed: {
    userGoal () {
      return this.$store.state.userInfo.goal
    },
    isFolder: function () {
      return this.competency.children &&
        this.competency.children.length
    },
    competencyId: function () {
      let identifier = this.competency['@id']
      var id_parts = identifier.split('/')
      return id_parts[id_parts.length-1]
    }
  },
  methods: {
    async setGoal() {
      this.$store.commit('setLearnerGoal', this.competency['@id'])
      let result = await this.$store.dispatch('patchLearnerGoal', this.$store.state.userInfo.goal);
      console.log("Set learner goal to" + this.$store.state.userInfo.goal);
    }
  }
}
</script>

<style>
  .badge {
    color: gold;
  }
</style>
