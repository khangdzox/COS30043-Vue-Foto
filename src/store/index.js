import { createStore } from 'vuex'

export default createStore({
  state () {
    return {
      user: {
        id: 1,
      }
    }
  },
  getters: {
  },
  mutations: {
    logout (state) {
      state.user = null
    },
    login (state, id) {
      state.user = { id }
    }
  },
  actions: {
  },
  modules: {
  }
})
