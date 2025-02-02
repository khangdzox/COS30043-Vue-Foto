<template>
  <div class="row post-container mx-2">
    <!-- Image -->
    <div class="col-12 col-md-7 post-image">
      <img :src="post.img" class="img-fluid" alt="Responsive image">
    </div>

    <!-- Content -->
    <div class="col-12 col-md-5 post-content">
      <!-- Title -->
      <h1>{{ post.title }}</h1>

      <!-- Tags -->
      <HorizontalList :key="post.tags" parent-bg-color="#FFFFFF">
        <TagPill fontSize="12" v-for="tag in post.tags?.split(',')" :key="tag">
          <router-link to="/">{{ tag }}</router-link>
        </TagPill>
      </HorizontalList>

      <!-- Post Content -->
      <p>{{ post.content }}</p>

      <!-- Author, Time, Follow Button -->
      <div class="row g-2">
        <!-- Author -->
        <div class="col-auto">
          <UserAvatar :userId="author.id" :size="48" :key="author.id"/>
        </div>

        <!-- Time -->
        <div class="col m-0 d-flex flex-column justify-content-center align-items-start">
          <span class="post-author-name">{{ author.name }}</span>
          <span class="post-time">{{ post.posted }}</span>
        </div>

        <!-- Edit button -->
        <div v-if="$store.state.user?.id == author.id" class="col-auto m-0 d-flex justify-content-center align-items-center">
          <router-link :to="`/post/${this.id}/edit`" class="btn post-edit-btn">
            <i class="bi bi-pencil-fill"></i>&nbsp;
            Edit
          </router-link>
        </div>

        <!-- Follow Button -->
        <div v-else class="col-auto m-0 d-flex justify-content-center align-items-center">
          <button v-if="followed" class="btn post-follow-btn" @click="unfollowAuthor()">Followed</button>
          <button v-else class="btn post-follow-btn" @click="followAuthor()">Follow</button>
        </div>
      </div>

      <!-- Like, Save, Share Buttons -->
      <div class="row g-1 post-fn-btn-container">
        <!-- Like -->
        <div class="col">
          <button to="#" class="btn post-fn-btn text-nowrap" @click="likePost()">
            <i v-if="!liked" class="bi bi-heart"></i>
            <i v-else class="bi bi-heart-fill"></i>&nbsp;
            <span>{{ heart }}</span>
          </button>
        </div>

        <!-- Save -->
        <div class="col">
          <button to="#" class="btn post-fn-btn text-nowrap" @click="savePost()">
            <template v-if="saved">
              <i class="bi bi-bookmark-fill"></i>&nbsp;
              <span>Saved</span>
            </template>
            <template v-else>
              <i class="bi bi-bookmark"></i>&nbsp;
              <span>Save</span>
            </template>
          </button>
        </div>

        <!-- Share -->
        <div class="col">
          <button to="#" class="btn post-fn-btn text-nowrap" @click="sharePost()">
            <i class="bi bi-share"></i>&nbsp;
            <span>Share</span>
          </button>
        </div>
      </div>

      <!-- Comments -->
      <CommentContainer :postId="post.id" :key="post.id"/>

    </div>
  </div>
</template>

<script>
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
  async mounted () {
    const post_res = await fetch(`/api/posts/${this.id}`)
    this.post = await post_res.json()

    const author_res = await fetch(`/api/users/${this.post.authorId}`)
    this.author = await author_res.json()

    const likes_count_res = await fetch(`/api/posts/${this.post.id}/likes`)
    this.heart = await likes_count_res.json()
    this.heart = this.heart.count

    if (this.$store.state.user) {
      const liked_res = await fetch(`/api/posts/${this.post.id}/likes/${this.$store.state.user.id}`)
      this.liked = await liked_res.json()
      this.liked = this.liked.liked

      const saved_res = await fetch(`/api/posts/${this.post.id}/saved/${this.$store.state.user.id}`)
      this.saved = await saved_res.json()
      this.saved = this.saved.saved

      const followed_res = await fetch(`/api/users/${this.$store.state.user.id}/follows/${this.author.id}`)
      this.followed = await followed_res.json()
      this.followed = this.followed.followed
    }
  },
  data () {
    return {
      post: {},
      author: {},
      heart: 0,
      liked: false,
      saved: false,
      followed: false
    }
  },
  methods: {
    async followAuthor() {
      if (!this.checkLogin()) return

      const follow_res = await fetch(`/api/users/${this.$store.state.user.id}/follows/${this.author.id}`, {
        method: 'POST'
      })
      this.followed = await follow_res.json()
      this.followed = this.followed.followed
    },
    unfollowAuthor() {
      if (!this.checkLogin()) return

      const unfollow_res = fetch(`/api/users/${this.$store.state.user.id}/follows/${this.author.id}`, {
        method: 'DELETE'
      })
      this.followed = false
    },
    likePost() {
      if (!this.checkLogin()) return

      if (this.liked) {
        this.heart -= 1

        const unlike_res = fetch(`/api/posts/${this.post.id}/likes/${this.$store.state.user.id}`, {
          method: 'DELETE'
        })
        this.liked = false;
      } else {
        this.heart += 1;

        const like_res = fetch(`/api/posts/${this.post.id}/likes/${this.$store.state.user.id}`, {
          method: 'POST'
        })
        this.liked = true;
      }
    },
    savePost() {
      if (!this.checkLogin()) return

      if (this.saved) {
        const unsave_res = fetch(`/api/posts/${this.post.id}/saved/${this.$store.state.user.id}`, {
          method: 'DELETE'
        })
        this.saved = false;
      } else {
        const save_res = fetch(`/api/posts/${this.post.id}/saved/${this.$store.state.user.id}`, {
          method: 'POST'
        })
        this.saved = true;
      }
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
  margin-top: 20px;
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

.post-edit-btn {
  font-weight: 600;
  font-size: 14px;
  padding: 4px 10px;
  background-color: #D9D9D9;
  color: #404040;
  border-radius: 24px;
}
.post-edit-btn:hover {
  background-color: #BFBFBF;
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
