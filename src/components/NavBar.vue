<template>
  <nav class="navbar navbar-light bg-light sticky-top">
    <div class="container-fluid">
      <!-- Brand -->
      <router-link to="/" class="brand">Foto</router-link>

      <!-- Search bar -->
      <SearchBar/>

      <!-- User avatar if logged in -->
      <div v-if="this.$store.state.user" ref="navbar-avatar" v-dropdown-togglable>
        <UserAvatar class="dropdown" :userId="this.$store.state.user.id"/>

        <!-- Dropdown menu -->
        <ul class="dropdown-menu">
          <li>
            <router-link :to="`/user/${this.$store.state.user.id}`" class="dropdown-item">Profile</router-link>
          </li>
          <li>
            <router-link to="#" class="dropdown-item" @click.prevent="$store.commit('setUser', null)">Logout</router-link>
          </li>
        </ul>
      </div>

      <!-- Login button if not logged in -->
      <router-link v-else to="/login" class="btn rounded-pill login-btn">Login</router-link>
    </div>
  </nav>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'
import UserAvatar from './UserAvatar.vue';

const dropdownTogglable = {
  mounted(el) {
    el.addEventListener('mouseenter', () => {
      el.querySelector('.dropdown-menu').classList.add('show')
    })
    el.addEventListener('mouseleave', () => {
      el.querySelector('.dropdown-menu').classList.remove('show')
    })
  }
}

export default {
  name: 'NavBar',
  components: {
    SearchBar,
    UserAvatar
  },
  directives: {
    dropdownTogglable
  },
  mounted() {
    // Add shadow to navbar on scroll
    window.onscroll = () => {
      const navbar = document.querySelector('.navbar')
      if (window.scrollY > 0) {
        navbar.classList.add('shadow')
      } else {
        navbar.classList.remove('shadow')
      }
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #f5f5f5 !important;
  transition: 0.3s;
}

.brand {
  font-family: 'Lemon';
  font-size: 30px;
  font-weight: 400;
  background: linear-gradient(141.67deg, #D79A61 21.6%, #FF3131 49.72%, #A260F5 78.4%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.dropdown-menu {
  margin-top: 0; /* remove the gap so it doesn't close */
  right: 0;
}

@property --gradient-color-1 {
  syntax: "<color>";
  initial-value: #D79A61;
  inherits: false;
}
@property --gradient-color-2 {
  syntax: "<color>";
  initial-value: #FF3131;
  inherits: false;
}
@property --gradient-color-3 {
  syntax: "<color>";
  initial-value: #A260F5;
  inherits: false;
}

.login-btn {
  background: linear-gradient(141.67deg, var(--gradient-color-1) 21.6%, var(--gradient-color-2) 49.72%, var(--gradient-color-3) 78.4%);
  color: #fff;
  font-weight: 600;
  transition: --gradient-color-1 0.3s, --gradient-color-2 0.3s, --gradient-color-3 0.3s;
}
.login-btn:hover {
  --gradient-color-1: #FF3131;
  --gradient-color-2: #A260F5;
  --gradient-color-3: #D79A61;
  color: #fff;
}
</style>
