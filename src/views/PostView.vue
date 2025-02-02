<template>
  <PostContainer :id="this.$route.params.postId" :key="this.$route.params.postId" />
  <h3 class="text-center" :key="posts">Similar to <strong>{{ posts.find(post => post.id == this.$route.params.postId)?.title }}</strong></h3>
  <MasonryContainer gap="20" :posts="posts" :key="posts"/>
</template>

<script>
import PostContainer from '@/components/PostContainer.vue'
import MasonryContainer from '@/components/MasonryContainer.vue'

export default {
  name: 'PostView',
  components: {
    PostContainer,
    MasonryContainer
  },
  async mounted () {
    const posts_res = await fetch(`/api/posts`)
    console.log(posts_res)
    this.posts = await posts_res.json()
  },
  data () {
    return {
      posts: []
    }
  },
}
</script>

<style scoped>
</style>
