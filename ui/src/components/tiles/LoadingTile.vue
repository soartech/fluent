<template>
  <v-card style="margin-top: 30px;">
    <v-container fluid>
      <v-layout row text-xs-center>
        <v-flex>
          <v-progress-circular
            :size="70"
            :width="3"
            color="blue"
            indeterminate
          ></v-progress-circular>
        </v-flex>
      </v-layout>
      <v-layout row text-xs-center>
        <v-flex>
          <h3 style="font-weight: normal; font-style: italic;">{{ loadingText }}</h3>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
export default {
  props: {
    loadingText: String
  }
}
</script>
