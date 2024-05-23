<template>
  <div class="home">
    <MasonryContainer :gap="20" v-slot="masonry">
      <PostThumbnail v-for="p in posts" :key="p.title"
      :title="p.title"
      :img="p.img"
      @image-loaded="masonry.arrange()"
      />
    </MasonryContainer>
  </div>
</template>

<script>
// @ is an alias to /src
import MasonryContainer from '@/components/MasonryContainer.vue'
import PostThumbnail from '@/components/PostThumbnail.vue'

export default {
  name: 'HomeView',
  components: {
    MasonryContainer,
    PostThumbnail
  },
  data () {
    return {
      posts: [
        {
          title: 'Post 1',
          img: 'https://picsum.photos/id/94/400/300'
        },
        {
          title: 'Post 2',
          img: 'https://picsum.photos/id/95/520/300'
        },
        {
          title: 'Post 3',
          img: 'https://picsum.photos/id/96/410/300'
        },
        {
          title: 'Post 4',
          img: 'https://picsum.photos/id/100/550/300'
        },
        {
          title: 'Post 5',
          img: 'https://picsum.photos/id/98/490/300'
        },
        {
          title: 'Post 6',
          img: 'https://picsum.photos/id/99/670/300'
        },
        {
          title: 'Post 7',
          img: 'https://picsum.photos/id/74/430/300'
        },
        {
          title: 'Post 8',
          img: 'https://picsum.photos/id/75/660/300'
        },
        {
          title: 'Post 9',
          img: 'https://picsum.photos/id/76/450/300'
        },
        {
          title: 'Post 10',
          img: 'https://picsum.photos/id/77/700/300'
        }
      ]
    }
  }
}
</script>
