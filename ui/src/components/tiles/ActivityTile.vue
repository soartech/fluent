<template>
  <v-flex xs4 md3 lg2>
    <v-badge style="width:100%:" :class="badgeClass" right overlap>
      <span slot="badge"></span>
        <v-card :class="highlightMethod()" @click.native="setIdx(index)">
          <v-flex xs12 lg12>
            <v-card-title style="padding: 2px;" primary-title>
              <div style="width: 100%">
                <h4 style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ title }}</h4>
              </div>
            </v-card-title>
          </v-flex>
          <v-layout style="min-height: 150px;" text-xs-center>
            <v-flex xs12 class="pa-2" text-xs-center justify-center>
                <v-card-media
                  :src="encodedURI"
                  height="150px"
                  style="width: 75%; margin: auto;"
                  contain
                ><h4 v-if="!imageExists">{{ title }}</h4></v-card-media>
              
            </v-flex>
          </v-layout>
        </v-card>
      </v-badge>
  </v-flex>
</template>

<script>
export default {
  props: {
    identifier: String,
    title: String,
    description: String,
    imageSrc: {
      type: String
    },
    index: {
      type: Number
    },
    setIdx: {
      type: Function
    },
    selected: {
      type: Boolean
    },
    tokens: {
      type: Number
    },
    launched: Boolean
  },
  data () {
    return {
      imgExistBool: true
    }
  },
  computed: {
    badgeClass() {
      if(this.tokens > 0 && !this.launched)
        return "whiteBadge"
      else
        return "blackBadge"
    },
    encodedURI () {
      return this.imageSrc
    },
    imageExists () {
      var img = new Image()

      img.onload = function () {
        this.imgExistBool = true
      }.bind(this)
      img.onerror = function () {
        this.imgExistBool = false
      }.bind(this)

      img.src = this.encodedURI

      return this.imgExistBool
    }
  },
  methods: {
    highlightMethod() {
      var classString = "activityCard";
      if (this.selected) {
        classString += " selectedClass";
      }
      return classString;
    }
  }
}
</script>

<style>
  .activityCard:hover {
    cursor: pointer;
  }
  .selectedClass {
    background-color: lightgray !important;
  }
  .whiteBadge {
    width: 100%
  }
  .whiteBadge > span {
    background-color: #FAFAFA !important;
    border: 2px solid #232B2B !important;
    padding:10px;
    border-radius: 25px;
  }
  .blackBadge > span {
    background-color: #232B2B !important;
    border: 2px solid #FAFAFA !important;
    padding:10px;
    border-radius: 25px;
  }
  .blackBadge {
    width: 100%
  }
</style>
