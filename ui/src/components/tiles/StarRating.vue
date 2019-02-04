<template>
  <!-- found this on codepen here: https://codepen.io/olimorris/pen/yOYBjd (modified slightly to suit our uses)-->
  <div class="star-rating">
        <label class="star-rating__star" v-for="(rating, i) in ratings" :key="i" :class="{'is-selected': ((value >= rating) && value != null), 'is-disabled': disabled}" v-on:click="set(rating)" v-on:mouseover="star_over(rating)" v-on:mouseout="star_out">
        <input class="star-rating star-rating__checkbox" type="radio" :value="rating" :name="name" v-model="value" :disabled="disabled">★</label></div>
</template>
<script>
export default {
  data: function() {
    return {
      temp_value: null,
      ratings: [1, 2, 3, 4, 5],
      value: this.setterValue
    }
  },
  props: {
    name: String,
    setterValue: null,
    id: String,
    disabled: Boolean,
    required: Boolean,
    setterFunc: Function
  },
  methods: {
    star_over: function(index) {
      var self = this;

      if (!this.disabled) {
        this.temp_value = this.value;
        return this.value = index;
      }

    },

    star_out: function() {
      var self = this;

      if (!this.disabled) {
        return this.value = this.temp_value;
      }
    },

    set: function(value) {
      var self = this;

      if (!this.disabled) {
        this.temp_value = value;
        this.setterFunc(value);
        return this.value = value;
      }
    }
  }
}
</script>

<style>
  .star-rating__star {
      display: inline-block;
      padding: 3px;
      vertical-align: middle;
      line-height: 1;
      font-size: 1.5em;
      color: #ABABAB;
      transition: color .2s ease-out;
  }

  .star-rating__star:hover {
    cursor: pointer;
  }

  .star-rating__star.is-selected {
    color: #FFD700;
  }

  .star-rating.is-disabled:hover {
    cursor: default
  }

  input[type="radio"] {
    display: none
  }
</style>

