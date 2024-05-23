<template>
  <div class="thumbnail">
    <img class="thumbnail-img" :src="this.img" @load="$emit('imageLoaded')">
    <h3 class="thumbnail-title">{{ title }}</h3>
  </div>
</template>

<script>
export default {
  name: 'PostThumbnail',
  props: {
    title: {
      type: String,
      default: 'Post Title'
    },
    img: {
      type: String,
      default: 'https://picsum.photos/200/200?random=0'
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

.thumbnail {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  overflow: hidden;
  padding: 0px;
  gap: 10px;
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
}
</style>
