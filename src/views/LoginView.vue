<template>
  <div class="row justify-content-center">
    <form class="col-12 col-md-6 p-3 login-form" @submit.prevent="submitForm" novalidate>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" name="email" id="email" v-model="email" ref="email-input" required>
        <div class="invalid-feedback fw-bold d-block">
          {{ formValidateMsg.email }}
        </div>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" name="password" id="password" v-model="password" ref="pw-input" required>
        <div class="invalid-feedback fw-bold d-block">
          {{ formValidateMsg.password }}
        </div>
      </div>
      <div class="mb-3">
        <div class="form-text">
          Don't have an account? <router-link to="/register">Register</router-link>
        </div>
      </div>
      <div v-show="loginMsg != ''" class="mb-3 alert alert-danger" role="alert">
        {{ loginMsg }}
      </div>
      <div class="mb-3 d-flex justify-content-center">
        <button type="submit" class="btn btn-primary">
          <i class="bi bi-box-arrow-in-right"></i>&nbsp;
          Login
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      loginMsg: '',
      formValidateMsg: {
        email: '',
        password: ''
      }
    }
  },
  mounted() {
    if (this.$store.state.user) {
      this.$router.push('/')
    }
  },
  methods: {
    async submitForm() {
      if (this.email === '') {
        this.formValidateMsg.email = 'Email is required'
      } else if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email) === false) {
        this.formValidateMsg.email = 'Invalid email format'
      } else {
        this.formValidateMsg.email = ''
      }

      if (this.password === '') {
        this.formValidateMsg.password = 'Password is required'
      } else {
        this.formValidateMsg.password = ''
      }

      if (!(this.formValidateMsg.email === '' && this.formValidateMsg.password === '')) {
        return
      }

      const res = await fetch(
        `/api/login`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        }
      )
      if (res.ok) {
        const user = await res.json()
        if (user) {
          this.$store.commit('setUser', user)
          this.$router.back()
        } else {
          this.loginMsg = 'Invalid email or password'
        }
      }
    }
  }
}
</script>

<style scoped>
.login-form {
  background-color: #fff;
  border-radius: 30px;
  box-shadow: 20px 20px 60px #d9d9d9, -20px -20px 60px #ffffff;
}
.form-label:has(+ :required)::after {
  content: ' *';
  color: red;
}
</style>