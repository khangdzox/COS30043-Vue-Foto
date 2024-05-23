<template>
  <form class="d-flex search-bar-container">
    <input type="search" class="search-bar form-control me-2" placeholder="Search" aria-label="Search">
    <button class="search-btn" type="submit">
      <i class="bi bi-search"></i>
    </button>
  </form>
</template>

<style scoped>
.search-bar-container {
  position: relative;
}
.search-bar {
  width: 100%;
  background: #FFFFFF;
  border-radius: 50px;
}
.search-btn {
  position: absolute;
  top: 2px;
  right: 10px;
  border: none;
  border-radius: 50px;
  padding: 5px 10px;
}
</style>
