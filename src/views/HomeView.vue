<template>
  <div class="row">
    <div class="col">
      <HorizontalList>
        <TagPill fontSize="20" v-for="tag in tags" :key="tag">
          <router-link to="/">{{ tag }}</router-link>
        </TagPill>
      </HorizontalList>
      <MasonryContainer gap="20" v-slot="masonry">
        <PostThumbnail v-for="p in posts"
          :key="p.title"
          :id="p.id"
          @image-loaded="masonry.arrange()"
        />
      </MasonryContainer>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import MasonryContainer from '@/components/MasonryContainer.vue'
import PostThumbnail from '@/components/PostThumbnail.vue'
import Posts from '@/assets/posts.json'
import HorizontalList from '@/components/HorizontalList.vue'
import TagPill from '@/components/TagPill.vue'

export default {
  name: 'HomeView',
  components: {
    MasonryContainer,
    PostThumbnail,
    HorizontalList,
    TagPill
  },
  data () {
    return {
      posts: Posts,
      tags: ['All', 'Nature', 'People', 'Tech', 'Animals', 'Architecture', 'Food', 'Travel', 'Fashion', 'Health', 'Art', 'Business', 'Education', 'Fitness', 'Music', 'Sports']
    }
  }
}
</script>
