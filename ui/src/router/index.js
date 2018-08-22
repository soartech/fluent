import Vue from 'vue'
import Router from 'vue-router'
import ErrorPage from '@/components/pages/404'
import LearnerApp from '@/apps/LearnerApp'
import FrameworkChooser from '@/components/pages/FrameworkChooser'
import ActivityChooser from '@/components/pages/ActivityChooser'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: LearnerApp,
      children: [
        {
          path: '/',
          component: FrameworkChooser
        },
        {
          path: 'activities',
          component: ActivityChooser
        },
        {
          path: 'activities/:id',
          component: ActivityChooser
        }
      ]
    },
    {
      path: '/',
      name: '404',
      component: ErrorPage
    }
  ]
})
