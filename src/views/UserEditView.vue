<template>
  <form class="p-3 user-edit-form" @submit.prevent="submitForm" @reset.prevent="discardForm">
    <div class="mb-3">
      <label for="name" class="form-label">Name</label>
      <input type="text" class="form-control" id="name" name="name" v-model="name">
      <div class="invalid-feedback fw-bold d-block">
        {{ formValidateMsg.email }}
      </div>
    </div>
    <div class="mb-3">
      <label for="email" class="form-label">Email</label>
      <input type="email" class="form-control" id="email" name="email" v-model="email">
      <div class="invalid-feedback fw-bold d-block">
        {{ formValidateMsg.email }}
      </div>
    </div>
    <div class="mb-3">
      <label for="img" class="form-label">User Image URL</label>
      <input type="url" class="form-control" id="img" name="img" v-model="img">
      <div class="user-img mt-2">
        <img class="w-100 h-100" v-if="img" :src="img" alt="Post Image">
        <div class="w-100 h-100 position-relative post-img-placeholder" v-else>
          <i class="bi bi-image position-absolute top-50 start-50 translate-middle post-img-placeholder-icon"></i>
        </div>
      </div>
    </div>
    <div class="mb-3">
      <label for="bgimg" class="form-label">Background Image URL</label>
      <input type="url" class="form-control" id="bgimg" name="bgimg" v-model="bgimg">
      <div class="user-bgimg mt-2">
        <img class="w-100 h-100" v-if="bgimg" :src="bgimg" alt="Post Image">
        <div class="w-100 h-100 position-relative post-img-placeholder" v-else>
          <i class="bi bi-image position-absolute top-50 start-50 translate-middle post-img-placeholder-icon"></i>
        </div>
      </div>
    </div>
    <div class="mb-3">
      <label for="desc" class="form-label">Description</label>
      <textarea class="form-control" id="desc" name="desc" v-model="desc" @input="(event) => event.target.style.height = event.target.scrollHeight + 'px'"></textarea>
    </div>
    <div class="mb-3 d-flex flex-wrap gap-3">
      <button type="reset" class="btn btn-secondary">
        <i class="bi bi-arrow-counterclockwise"></i>&nbsp;
        Discard
      </button>
      <button type="submit" class="btn btn-primary">
        <i class="bi bi-check2"></i>&nbsp;
        Submit
      </button>
    </div>
  </form>
</template>

<script>
export default {
  name: 'UserEditView',
  data() {
    return {
      name: '',
      email: '',
      img: '',
      bgimg: '',
      desc: '',
      formValidateMsg: {
        name: '',
        email: ''
      }
    }
  },
  async mounted() {
    if (!this.$store.state.user) {
      this.$router.push('/login')
    }
    const user_res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/users/${this.$store.state.user.id}`)
    const user = await user_res.json()
    this.name = user.name
    this.email = user.email
    this.img = user.img
    this.bgimg = user.bgImg
    this.desc = user.about
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

      if (!(
        this.formValidateMsg.name === '' &&
        this.formValidateMsg.email === '')
      ) {
        return
      }

      const user_res = await fetch(
        `${process.env.VUE_APP_API_BASE_URL}/api/users/${this.$store.state.user.id}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            img: this.img,
            bgImg: this.bgimg,
            about: this.desc
          })
        }
      )
      const user = await user_res.json()
      this.$store.commit('setUser', user)
      this.$router.push(`/user/${this.$store.state.user.id}`)
    },
    discardForm() {
      if (!confirm('Discard changes?')) {
        return
      }
      this.$router.push(`/user/${this.$store.state.user.id}`)
    }
  }
}
</script>

<style scoped>
.user-edit-form {
  background-color: #FFFFFF;
  border-radius: 30px;
  box-shadow: 20px 20px 60px #d9d9d9, -20px -20px 60px #ffffff;
}
.user-img {
  width: 200px;
  height: 200px;
  border-radius: 24px;
  overflow: hidden;
}
.user-bgimg {
  width: 100%;
  height: 200px;
  border-radius: 24px;
  overflow: hidden;
}
.user-img img,
.user-bgimg img {
  object-fit: cover;
  object-position: center;
}
.post-img-placeholder {
  background: linear-gradient(135deg, #D9D9D9 0%, #F5F5F5 59.5%, #FFFFFF 100%);
  border-radius: 24px;
}
.post-img-placeholder-icon {
  font-size: 60px;
  color: #6c757d;
}
</style>