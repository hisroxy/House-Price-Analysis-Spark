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
    fetchDashboardData({ commit }) {
      // 模拟静态数据
      const userData = {
        totalUsers: 1234,
        activeUsers: 856,
        newUserCount: 45,
        avgSessionTime: '12:34'
      }
      
      const recommendationData = [
        { id: 1, title: '深圳南山科技园三居室', price: '8500元/月', score: 9.2 },
        { id: 2, title: '广州天河CBD精装公寓', price: '6800元/月', score: 8.8 },
        { id: 3, title: '上海浦东新区学区房', price: '12000元/月', score: 9.5 }
      ]
      
      const dashboardData = {
        totalHouses: 15678,
        avgPrice: 7800,
        priceTrend: [6500, 6800, 7200, 7500, 7800, 8200],
        areaDistribution: [
          { name: '深圳', value: 35 },
          { name: '广州', value: 28 },
          { name: '上海', value: 22 },
          { name: '北京', value: 15 }
        ]
      }
      
      commit('SET_USER_STATS', userData)
      commit('SET_RECOMMENDATION_PREVIEW', recommendationData)
      commit('SET_DASHBOARD_DATA', dashboardData)
    }
  },
  modules: {
  }
})