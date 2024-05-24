<template>
  <router-link :to="`/user/${userId}`" class="user-avatar">
    <img v-if="src" :src="src" class="user-img"/>
    <i v-else class="bi bi-person-fill user-no-img"></i>
  </router-link>
</template>

<script>
import Users from '@/assets/users.json'

export default {
  name: 'UserAvatar',
  props: {
    userId: {
      type: Number,
      required: true
    },
    size: {
      type: Number,
      default: 60
    },
  },
  data () {
    return {
      src: Users.find(user => user.id === this.userId)?.img
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
}
.user-no-img {
  font-size: v-bind(size + 'px');
  background: linear-gradient(141.67deg, #D79A61 21.6%, #FF3131 49.72%, #A260F5 78.4%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
