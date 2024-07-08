import { createStore } from 'vuex'

export default createStore({
  state () {
    return {
      user: null,
      query: ''
    }
  },
  getters: {
  },
  mutations: {
    delUser (state) {
      state.user = null
    },
    setUser (state, user) {
      state.user = user
    },
    delQuery (state) {
      state.query = ''
    },
    setQuery (state, query) {
      state.query = query
    }
  },
  actions: {
  },
  modules: {
  }
})
