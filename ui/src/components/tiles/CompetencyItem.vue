<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12 sm8>
        <span @click="toggle" :class="{bold: isFolder}" style="font-size: 18px;"><span v-if="isFolder">{{ open ? '&#9660;' : '&#9658;' }}</span>{{ competency['ceasn:codedNotation'] }} {{ competency.name }} <span>{{ held ? '(Held)' : '(Not Held)' }}</span>
        </span>
      </v-flex>
      <v-flex xs12 sm4 text-xs-right>
        <v-btn :to="'activities/'+competencyId">Go</v-btn>
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
    held: Boolean
  },
  computed: {
    isFolder: function () {
      return this.competency.children &&
        this.competency.children.length
    },
    competencyId: function () {
      let identifier = this.competency['@id']
      var id_parts = identifier.split('/')
      return id_parts[id_parts.length-1]
    }
  }
}
</script>
