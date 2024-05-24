<template>
  <div class="row post-container mx-2">
    <div class="col-12 col-md-7 post-image">
      <img :src="post.img" class="img-fluid" alt="Responsive image">
    </div>

    <div class="col-12 col-md-5 post-content">
      <h1>{{ post.title }}</h1>

      <HorizontalList>
        <TagPill fontSize="12" v-for="tag in post.tags" :key="tag">
          <router-link to="/">{{ tag }}</router-link>
        </TagPill>
      </HorizontalList>

      <p>{{ post.content }}</p>

      <div class="row g-2">
        <div class="col-auto">
          <UserAvatar :userId="author.id" :size="48"/>
        </div>

        <div class="col d-flex flex-column justify-content-center align-items-start">
          <span class="post-author-name">{{ author.name }}</span>
          <span class="post-time">{{ post.posted }}</span>
        </div>

        <div class="col-auto d-flex justify-content-center align-items-center">
          <router-link to="#" class="btn post-follow-btn" @click="followAuthor()">Follow</router-link>
        </div>
      </div>

      <div class="row g-1 post-fn-btn-container">
        <div class="col">
          <button to="#" class="btn post-fn-btn text-nowrap" @click="likePost()">
            <i v-if="!liked" class="bi bi-heart"></i>
            <i v-else class="bi bi-heart-fill"></i>&nbsp;
            <span>{{ heart }}</span>
          </button>
        </div>

        <div class="col">
          <button to="#" class="btn post-fn-btn text-nowrap" @click="savePost()">
            <i class="bi bi-bookmark"></i>&nbsp;
            <span>Save</span>
          </button>
        </div>

        <div class="col">
          <button to="#" class="btn post-fn-btn text-nowrap" @click="sharePost()">
            <i class="bi bi-share"></i>&nbsp;
            <span>Share</span>
          </button>
        </div>
      </div>

      <CommentContainer :postId="post.id"/>

    </div>
  </div>
</template>

<script>
import Posts from '@/assets/posts.json'
import Users from '@/assets/users.json'
import HorizontalList from '@/components/HorizontalList.vue'
import TagPill from '@/components/TagPill.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import CommentContainer from '@/components/CommentContainer.vue'

export default {
  name: 'PostContainer',
  props: ['id'],
  components: {
    HorizontalList,
    TagPill,
    UserAvatar,
    CommentContainer
  },
  data () {
    return {
      post: Posts.find(post => post.id == this.id),
      author: Users.find(user => user.id == Posts.find(post => post.id == this.id).authorId),
      heart: 100,
      liked: false,
    }
  },
  methods: {
    followAuthor() {
      if (!this.checkLogin()) return

      alert('Author followed');
    },
    likePost() {
      if (!this.checkLogin()) return

      if (this.liked) {
        this.heart -= 1;
      } else {
        this.heart += 1;
      }
      this.liked = !this.liked;
    },
    savePost() {
      if (!this.checkLogin()) return

      alert('Post saved');
    },
    sharePost() {
      if (!this.checkLogin()) return

      alert('Post shared');
    },
    checkLogin() {
      if (!this.$store.state.user) {
        alert('You must login to perform this action');
        return false
      }
      return true
    }
  },
}
</script>

<style scoped>
.post-container {
  background-color: #FFFFFF;
  padding: 32px 20px 22px 20px;
  border-radius: 48px;
  box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.25);
  margin-bottom: 40px;
}

.post-image img {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
  border-radius: 24px;
}

.post-content {
  text-align: left;
}
.post-content > * {
  margin-bottom: 10px;
}
.post-content h1 {
  font-family: 'Montserrat Alternates';
  font-style: normal;
  font-weight: 700;
  font-size: 36px;
  line-height: 44px;
  margin-top: 0;
}
.post-content p {
  font-weight: 400;
  font-size: 16px;
}

.post-author-name {
  font-weight: 600;
  font-size: 16px;
}
.post-time {
  font-weight: 400;
  font-size: 12px;
}

.post-follow-btn {
  font-weight: 600;
  font-size: 14px;
  padding: 4px 10px;
  background-color: #FD4949;
  color: #FFFFFF;
  border-radius: 24px;
}
.post-follow-btn:hover {
  background-color: #ca2828;
}
.post-follow-btn:active {
  background-color: #ff7474;
  border: 1px solid #ff7474;
}

.post-fn-btn-container {
  container: post-fn-btns / inline-size;
}
.post-fn-btn {
  width: 100%;
  padding: 4px 10px;
  font-weight: 600;
  font-size: 13px;
  text-align: center;
  background-color: #D9D9D9;
  color: #404040;
  border-radius: 24px;
}
.post-fn-btn:hover {
  background-color: #BFBFBF;
}
.post-fn-btn:active {
  background-color: #D9D9D9;
  border: 1px solid #D9D9D9;
}
@container post-fn-btns (max-width: 200px) {
  .post-fn-btn span {
    display: none;
  }
}
</style>
