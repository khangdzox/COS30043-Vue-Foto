<template>
  <PostContainer :id="this.$route.params.id" />
  <h3 class="text-center">Similar to <strong>{{ posts.find(post => post.id == this.$route.params.id).title }}</strong></h3>
  <MasonryContainer gap="20" v-slot="masonry">
    <PostThumbnail v-for="p in posts"
      :key="p.title"
      :id="p.id"
      @image-loaded="masonry.arrange()"
    />
  </MasonryContainer>
</template>

<script>
import Posts from '@/assets/posts.json'
import PostContainer from '@/components/PostContainer.vue'
import MasonryContainer from '@/components/MasonryContainer.vue'
import PostThumbnail from '@/components/PostThumbnail.vue'
import { post } from 'jquery';

export default {
  name: 'PostView',
  components: {
    PostContainer,
    MasonryContainer,
    PostThumbnail
  },
  data () {
    return {
      posts: Posts
    }
  },
}
</script>

<style scoped>
</style>
