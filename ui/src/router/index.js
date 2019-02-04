import Vue from 'vue'
import Router from 'vue-router'
import ErrorPage from '@/components/pages/404'
import LearnerApp from '@/apps/LearnerApp'
import ActivityChooser from '@/components/pages/ActivityChooser'
import CompetencyTree from '@/components/pages/CompetencyTree'
import Admin from '@/components/pages/Admin'
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
          component: CompetencyTree
        },
        {
          path: 'activities',
          component: ActivityChooser,
          children: [
            {
              path: 'all'
            },
            {
              path: 'focused'
            }
          ]
        },
        {
          path: '/admin',
          component: Admin
        }
      ]
    },
    {
      path: '/*',
      name: '404',
      component: ErrorPage
    }
  ]
})
