<template>
  <div class="row">
    <div class="col">

      <HorizontalList :key="tags">
        <TagPill fontSize="20" v-for="tag in tags" :key="tag">
          <div @click="$store.commit('setQuery', tag)">{{ tag }}</div>
        </TagPill>
      </HorizontalList>

      <MasonryContainer gap="20" :posts="posts" :key="posts"/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import MasonryContainer from '@/components/MasonryContainer.vue'
import HorizontalList from '@/components/HorizontalList.vue'
import TagPill from '@/components/TagPill.vue'

export default {
  name: 'HomeView',
  components: {
    MasonryContainer,
    HorizontalList,
    TagPill
  },
  async mounted () {
    const posts_res = await fetch(`/api/posts`)
    this.posts = await posts_res.json()

    const tags_res = await fetch(`/api/tags`)
    this.tags = await tags_res.json()
  },
  watch: {
    async '$store.state.query' () {
      var query = this.$store.state.query
      if (query !== '') {
        const posts_res = await fetch(`/api/posts`)
        this.posts = await posts_res.json()
        this.posts = this.posts.filter(post => {
          return post.tags?.includes(query) || post.title.toLowerCase().includes(query.toLowerCase()) || post.content.toLowerCase().includes(query.toLowerCase())}
        )
      } else {
        const posts_res = await fetch(`/api/posts`)
        this.posts = await posts_res.json()
      }
    }
  },
  data () {
    return {
      posts: [],
      tags: []
    }
  }
}
</script>
