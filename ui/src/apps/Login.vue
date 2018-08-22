<template>
<div>
    <v-app>
      <v-container>
        <v-layout row align-center justify-center text-xs-center class="pa-5">
          <v-flex xs12 sm6>
            <v-card>

              <v-card-title primary-title>
                <div>
                  <h3 class="headline mb-0">FLUENT Login</h3>
                </div>
              </v-card-title>

              <v-card-actions>
                <v-layout>
                  <v-flex xs12 align-center>
                    <v-btn color="blue" :to="'/'">Login</v-btn>
                  </v-flex>
                </v-layout>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-app>
  </div>
</template>

<script>
  export default {
    methods: {
    }
  }
</script>