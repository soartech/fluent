<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <v-card>
          <v-layout style="min-height: 150px;">
            <v-flex xs6 lg2 class="pa-2" justify-center>
              <v-card-media
                :src=imageSrc
                height="150px"
                contain
              ></v-card-media>
            </v-flex>
            <v-flex xs6 lg10>
              <v-card-title primary-title>
                <div>
                  <a class="headline" :href="launchUrl" target="_blank">{{ title }}</a>
                  <div>{{ description }}</div>
                </div>
              </v-card-title>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  props: {
    imageSrc: {
      type: String
    },
    title: {
      type: String
    },
    description: {
      type: String
    },
    launchUrl: {
      type: String
    }
  }
}
</script>

