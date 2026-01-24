import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    houses: [],
    recommendations: []
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_HOUSES(state, houses) {
      state.houses = houses
    },
    SET_RECOMMENDATIONS(state, recommendations) {
      state.recommendations = recommendations
    }
  },
  actions: {
  },
  modules: {
  }
})