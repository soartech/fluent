<template>
  <v-container fluid>
    <v-layout>
      <v-list-group
            v-for="item in items"
            :key="item.title"
            no-action
          >
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>

            <v-list-tile
              v-for="subItem in item.items"
              :key="subItem.title"
            >
            <v-container>
              <v-layout>
                <v-flex>
                  <p> {{ subItem.title }} </p>
                </v-flex>
              </v-layout>
            </v-container>
              <v-list-tile-content>
                <v-list-tile-title>{{ subItem.title }}</v-list-tile-title>
              </v-list-tile-content>
                <list-group
                v-if="subItem.items"
                :items="subItem.items"></list-group>
            </v-list-tile>
          </v-list-group>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'list-group',
  props: {
    items: {
      type: Array
    }
  }
}
</script>

