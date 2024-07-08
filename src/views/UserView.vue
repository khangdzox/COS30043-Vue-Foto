<template>
  <div class="user-panel w-100 h-100 p-3">
    <div class="d-flex flex-column justify-content-center align-items-center gap-3">
      <UserAvatar class="user-img" :userId="user.id" :size="170" :key="user.id"/>
      <h1 class="user-name m-0">{{ user.name }}</h1>
      <div class="d-flex gap-3" v-if="$route.params.userId == $store.state.user?.id">
        <router-link :to="`/user/edit`" class="btn py-0 rounded-pill user-panel-btn">
          <i class="bi bi-pencil-fill"></i>&nbsp;
          Edit Profile
        </router-link>
        <router-link :to="`/post/new`" class="btn py-0 rounded-pill user-panel-btn">
          <i class="bi bi-plus-lg"></i>&nbsp;
          New Post
        </router-link>
      </div>
      <div class="d-flex gap-3" v-else>
        <button class="btn py-0 rounded-pill user-panel-btn">
          <i class="bi bi-heart-fill"></i>&nbsp;
          Follow
        </button>
      </div>
    </div>
  </div>
  <nav class="nav nav-tabs nav-fill mt-3">
      <button class="nav-link active" ref="user-nav-posts">
        <i class="bi bi-grid-3x3-gap-fill"></i>&nbsp;
        Posts
      </button>
      <button class="nav-link" ref="user-nav-saved">
        <i class="bi bi-bookmark-fill"></i>&nbsp;
        Saved
      </button>
      <button class="nav-link" ref="user-nav-about">
        <i class="bi bi-info-circle-fill"></i>&nbsp;
        About
      </button>
  </nav>
  <MasonryContainer v-if="tab=='posts'" :posts="user_posts" :key="user_posts" />
  <MasonryContainer v-if="tab=='saved'" :posts="saved_posts" :key="saved_posts" />
  <div v-if="tab=='about'" class="mt-3">
    <p>{{ user.about }}</p>
  </div>
</template>

<script>
import UserAvatar from '@/components/UserAvatar.vue'
import MasonryContainer from '@/components/MasonryContainer.vue';

export default {
  name: 'UserView',
  components: {
    UserAvatar,
    MasonryContainer
  },
  async mounted() {
    this.$refs['user-nav-posts'].addEventListener('click', () => {
      this.tab = 'posts'
      this.$refs['user-nav-posts'].classList.add('active')
      this.$refs['user-nav-saved'].classList.remove('active')
      this.$refs['user-nav-about'].classList.remove('active')
    })
    this.$refs['user-nav-saved'].addEventListener('click', () => {
      this.tab = 'saved'
      this.$refs['user-nav-posts'].classList.remove('active')
      this.$refs['user-nav-saved'].classList.add('active')
      this.$refs['user-nav-about'].classList.remove('active')
    })
    this.$refs['user-nav-about'].addEventListener('click', () => {
      this.tab = 'about'
      this.$refs['user-nav-posts'].classList.remove('active')
      this.$refs['user-nav-saved'].classList.remove('active')
      this.$refs['user-nav-about'].classList.add('active')
    })

    const user_res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/users/${this.$route.params.userId}`)
    this.user = await user_res.json()

    const user_posts_res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/users/${this.$route.params.userId}/posts`)
    this.user_posts = await user_posts_res.json()
    console.log(this.user_posts)

    const saved_res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/users/${this.$route.params.userId}/saved`)
    const saved_posts = await saved_res.json()
    this.saved_posts = []
    saved_posts.forEach(async post => {
      const post_res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/posts/${post.postId}`)
      this.saved_posts.push(await post_res.json())
    })
  },
  data() {
    return {
      user: {},
      user_posts: [],
      saved_posts: [],
      tab: 'posts'
    }
  }
}
</script>

<style scoped>
.user-panel {
  background: v-bind("`url('${user.bgImg}')`") no-repeat center center, #f5f5f5;
  background-size: cover;
  border-radius: 0px 0px 24px 24px;
}
.user-img {
  box-shadow: 0px -8px 10px #ffffffaa, 0px 5px 10px #00000055;
}
.user-name {
  font-size: 24px;
  font-weight: 600;
  background-color: #f5f5f5cc;
  padding-left: 10px;
  padding-right: 10px;
}
.user-panel-btn {
  background-color: #f5f5f5cc;
  font-weight: 500;
}
.nav-link {
  color: #000000;
}
.active {
  background: linear-gradient(to bottom, #e0e0e0, #f5f5f5) !important;
  border-bottom-color: #f5f5f5 !important;
}
</style>