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

// 配置CSRF令牌
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// 请求拦截器 - 自动添加CSRF令牌
axios.interceptors.request.use(
  config => {
    // 从cookie中获取CSRF令牌
    const csrfToken = getCookie('csrftoken')
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 获取cookie的辅助函数
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')