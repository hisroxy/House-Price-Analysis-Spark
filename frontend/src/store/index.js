import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userStats: {},                 // 用户统计数据
    recommendationPreview: [],     // 推荐预览数据
    dashboardData: {}             // 仪表板完整数据
  },
  mutations: {
    SET_USER_STATS(state, stats) {
      state.userStats = stats
    },
    SET_RECOMMENDATION_PREVIEW(state, recommendations) {
      state.recommendationPreview = recommendations
    },
    SET_DASHBOARD_DATA(state, data) {
      state.dashboardData = data
    }

  },
  actions: {
  },
  modules: {
  }
})