import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import axios from 'axios'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false
Vue.use(ElementUI)

// 配置axios
Vue.prototype.$http = axios
// axios.defaults.baseURL = '/'
axios.defaults.timeout = 10000

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')