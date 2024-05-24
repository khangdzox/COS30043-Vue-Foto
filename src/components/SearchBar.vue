<template>
  <form class="d-flex search-bar-container" @submit.prevent="search()">
    <div class="input-group">
      <input type="text" class="search-elem form-control" placeholder="Search" aria-label="Search" ref="search-input">
      <button class="btn search-elem" type="reset">
        <i class="bi bi-x-lg"></i>
      </button>
      <button class="btn search-elem" type="submit">
        <i class="bi bi-search"></i>
      </button>
    </div>
  </form>
</template>

<script>
export default {
  name: 'SearchBar',
  methods: {
    search() {
      const input = this.$refs['search-input']
      if (input.value) {
        alert(`You searched for ${input.value}`)
      }
    }
  }
}
</script>

<style scoped>
.search-bar-container {
  position: relative;
  width: 50%;
  background: #ffffff;
  box-shadow: 0px 0px 16px #d3d4d5;
  border: 1px solid #fff;
  border-radius: 50px;
  transition: 0.5s;
}
.search-elem {
  background: transparent;
  border: none;
  border-radius: 50px;
  transition: 0.5s;
}
.search-elem:hover {
  background: #f0f0f0;
  border-radius: 50px;
  transition: 0.5s;
}
</style>
