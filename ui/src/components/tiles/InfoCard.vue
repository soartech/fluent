<template>
  <v-card style="margin-top: 30px;">
    <v-container fluid>
      <v-layout row text-xs-center>
        <v-flex>
          <h2 style="font-weight: normal; font-style: italic;">{{ infoText }}</h2>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
export default {
  props: {
    infoText: String
  }
}
</script>
