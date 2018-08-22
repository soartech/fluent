// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import {
  Vuetify,
  VApp,
  VNavigationDrawer,
  VFooter,
  VList,
  VCard,
  VBtn,
  VIcon,
  VGrid,
  VExpansionPanel,
  VDivider,
  VToolbar,
  VBreadcrumbs,
  VAvatar,
  VForm,
  VTextField,
  VDataTable,
  VProgressLinear,
  VSelect,
  VCheckbox,
  VRadioGroup,
  VDialog,
  VProgressCircular,
  VTooltip,
  transitions
} from 'vuetify'
import '../node_modules/vuetify/src/stylus/app.styl'

import VueCookie from 'vue-cookie'

Vue.use(Vuetify, {
  components: {
    VApp,
    VNavigationDrawer,
    VFooter,
    VList,
    VCard,
    VBtn,
    VIcon,
    VGrid,
    VExpansionPanel,
    VDivider,
    VToolbar,
    VBreadcrumbs,
    VAvatar,
    VForm,
    VTextField,
    VDataTable,
    VProgressLinear,
    VSelect,
    VCheckbox,
    VRadioGroup,
    VDialog,
    VProgressCircular,
    VTooltip,
    transitions
  },
  theme: {
    primary: '#000',
    secondary: '#000',
    accent: '#000',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107'
  }
})

Vue.use(VueCookie)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
