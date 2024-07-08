<template>
  <div class="thumbnail">
    <router-link :to="`/post/${post.id}`">
      <img class="thumbnail-img" :src="post.img" @load="$emit('imageLoaded')">
      <h3 class="thumbnail-title mt-1">{{ post.title }}</h3>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'PostThumbnail',
  props: ['post'],
  data () {
    return {
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
  transition: 0.3s;
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
  font-size: 16px;
  line-height: 24px;
  text-align: left;
}
</style>
