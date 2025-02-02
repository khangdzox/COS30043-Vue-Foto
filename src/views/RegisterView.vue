<template>
  <div class="row justify-content-center">
    <form class="col-12 col-md-6 p-3 register-form" @submit.prevent="submitForm" novalidate>
      <div class="mb-3">
        <label for="name" class="form-label">User Name</label>
        <input type="text" class="form-control" name="name" id="name" v-model="name" ref="name-input" required minlength="3" maxlength="50">
        <div class="invalid-feedback fw-bold d-block">
          {{ formValidateMsg.name }}
        </div>
      </div>
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
        <label for="repassword" class="form-label">Re-type Password</label>
        <input type="password" class="form-control" name="repassword" id="repassword" v-model="repassword" ref="rpw-input" required>
        <div class="invalid-feedback fw-bold d-block">
          {{ formValidateMsg.repassword }}
        </div>
      </div>
      <div class="mb-3 form-check">
        <input type="checkbox" class="form-check-input" name="tnc" id="tnc" v-model="tnc" ref="tnc-input" required>
        <label for="tnc" class="form-check-label">I accept foto's Terms & Conditions</label>
        <div class="invalid-feedback fw-bold d-block">
          {{ formValidateMsg.tnc }}
        </div>
      </div>
      <div class="mb-3">
        <div class="form-text">
          Already have an account? <router-link to="/login">Login</router-link>
        </div>
      </div>
      <div v-show="registerMsg != ''" class="mb-3 alert alert-danger" role="alert">
        {{ registerMsg }}
      </div>
      <div class="mb-3 d-flex justify-content-center">
        <button type="submit" class="btn btn-primary">
          <i class="bi bi-box-arrow-in-right"></i>&nbsp;
          Register
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      repassword: '',
      tnc: false,
      registerMsg: '',
      formValidateMsg: {
        name: '',
        email: '',
        password: '',
        repassword: '',
        tnc: ''
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

      if (this.name === '') {
        this.formValidateMsg.name = 'Name is required'
      } else if (this.name.length < 3) {
        this.formValidateMsg.name = 'Name must be at least 3 characters long'
      } else if (this.name.length > 50) {
        this.formValidateMsg.name = 'Name must be at most 50 characters long'
      } else {
        this.formValidateMsg.name = ''
      }

      if (this.email === '') {
        this.formValidateMsg.email = 'Email is required'
      } else if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email) === false) {
        this.formValidateMsg.email = 'Invalid email format'
      } else {
        this.formValidateMsg.email = ''
      }

      if (this.password === '') {
        this.formValidateMsg.password = 'Password is required'
      } else if (this.password.length < 8) {
        this.formValidateMsg.password = 'Password must be at least 8 characters long'
      } else if (/^[a-zA-Z]+$/.test(this.password)) {
        this.formValidateMsg.password = 'Password must contain at least one number or special character'
      } else {
        this.formValidateMsg.password = ''
      }

      if (this.repassword === '') {
        this.formValidateMsg.repassword = 'Re-typed password is required'
      } else if (this.password !== this.repassword) {
        this.formValidateMsg.repassword = 'Re-typed password does not match'
      } else {
        this.formValidateMsg.repassword = ''
      }

      if (this.tnc === false) {
        this.formValidateMsg.tnc = 'You must accept the Terms & Conditions'
      } else {
        this.formValidateMsg.tnc = ''
      }

      if (!(
        this.formValidateMsg.name === '' &&
        this.formValidateMsg.email === '' &&
        this.formValidateMsg.password === '' &&
        this.formValidateMsg.repassword === '' &&
        this.formValidateMsg.tnc === '')
      ) {
        return
      }

      const res = await fetch(
        `/api/users`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            password: this.password
          })
        }
      )
      if (res.ok) {
        const user = await res.json()
        if (user) {
          this.$store.commit('setUser', user)
          this.$router.push('/')
        } else {
          this.registerMsg = 'Registration failed. Please try again later. Error: invalid user data'
        }
      } else {
        this.registerMsg = 'Registration failed. Please try again later. Error: ' + res.status + ' ' + res.statusText
      }
    }
  }
}
</script>

<style scoped>
.register-form {
  background-color: #fff;
  border-radius: 30px;
  box-shadow: 20px 20px 60px #d9d9d9, -20px -20px 60px #ffffff;
}
.form-label:has(+ :required)::after,
:required + .form-check-label:after {
  content: ' *';
  color: red;
}
</style>