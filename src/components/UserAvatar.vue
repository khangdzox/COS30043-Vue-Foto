<template>
  <router-link :to="`/user/${userId}`" class="user-avatar">
    <!-- Show user avatar -->
    <img v-if="src" :src="src" class="user-img"/>

    <!-- Show default avatar if user does not have avatar -->
    <i v-else class="bi bi-person-fill user-no-img"></i>
  </router-link>
</template>

<script>
export default {
  name: 'UserAvatar',
  props: {
    userId: {
      required: true
    },
    size: {
      type: Number,
      default: 60
    },
  },
  async mounted() {
    if (!this.userId) {
      return
    }

    const res = await fetch(`/api/users/${this.userId}`)
    const user = await res.json()
    this.src = user.img
  },
  data() {
    return {
      src: ''
    }
  },
}
</script>

<style scoped>
.user-avatar {
  display: inline-block;
  overflow: hidden;
  border-radius: 50%;
  background-color: #f0f0f0;
  width: v-bind(size + 'px');
  height: v-bind(size + 'px');
}
.user-img {
  width: v-bind(size + 'px');
  height: v-bind(size + 'px');
  object-fit: cover;
}
.user-no-img {
  font-size: v-bind(size + 'px');
  background: linear-gradient(141.67deg, #D79A61 21.6%, #FF3131 49.72%, #A260F5 78.4%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
