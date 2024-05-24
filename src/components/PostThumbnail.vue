<template>
  <div class="thumbnail">
    <router-link :to="`/post/${id}`">
      <img class="thumbnail-img" :src="this.img" @load="$emit('imageLoaded')">
      <h3 class="thumbnail-title mt-1">{{ title }}</h3>
    </router-link>
  </div>
</template>

<script>
import Posts from '@/assets/posts.json'

export default {
  name: 'PostThumbnail',
  props: ['id'],
  data () {
    return {
      title: Posts.find(post => post.id === this.id)?.title,
      img: Posts.find(post => post.id === this.id)?.img
    }
  }
}
</script>

<style scoped>
.thumbnail {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  overflow: hidden;
  padding: 0px;
  gap: 10px;
}
.thumbnail a {
  color: #000000;
  text-decoration: none;
}
.thumbnail-img {
  width: 100%;
  height: auto;
  overflow: hidden;
  border-radius: 24px;
}
.thumbnail-title {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  line-height: 24px;
  text-align: left;
}
</style>
