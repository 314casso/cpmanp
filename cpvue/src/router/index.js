import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Table1 from '@/components/Table'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/h',
      name: 'Hello',
      component: Hello,
      meta: {auth: true}
    },
    {
      path: '/t',
      name: 'Table',
      component: Table1,
      meta: {auth: true}
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
