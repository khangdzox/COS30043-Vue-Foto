<template>
  <nav class="navbar navbar-light bg-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Foto</router-link>
      <SearchBar/>
      <router-link to="/" class="navbar-brand"><i class="bi bi-person-fill"></i></router-link>
    </div>
  </nav>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'

export default {
  name: 'NavBar',
  components: {
    SearchBar
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lemon&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
.navbar-brand {
  font-family: 'Lemon';
  font-size: 30px;
  font-weight: 400;
  background: linear-gradient(141.67deg, #D79A61 21.6%, #FF3131 49.72%, #A260F5 78.4%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  /* text-fill-color: transparent; */
}
</style>
