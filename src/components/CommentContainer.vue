<template>
  <!-- Comment textbox -->
  <div class="row">
    <form class="col" @submit.prevent="addComment()">

      <!-- Show input if logged in -->
      <div v-if="this.$store.state.user" class="input-group comment-input">
        <input type="text" class="form-control" placeholder="Comment here..." ref="comment-input">
        <button class="btn" type="submit">
          <i class="bi bi-send"></i>
        </button>
      </div>

      <!-- Show disabled input if not logged in -->
      <div v-else class="input-group comment-input disabled">
        <input type="text" class="form-control" placeholder="You must login to comment" ref="comment-input" disabled>
      </div>
    </form>
  </div>

  <!-- Comments -->
  <template v-if="comments.length > 0">
    <div class="row g-2" v-for="comment in paginatedComments" :key="comment">
      <div class="col-auto">
        <UserAvatar :userId="comment.authorId" :size="32"/>
      </div>
      <div class="col">
        <div class="comment-name">{{ users.find(user => user.id == comment.authorId)?.name }}</div>
        <div class="comment-content">{{ comment.content }}</div>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <Paginate
        container-class="pagination"
        page-class="page-item"
        page-link-class="page-link"
        prev-class="page-item"
        prev-link-class="page-link"
        next-class="page-item"
        next-link-class="page-link"
        :page-count="pageCount"
        prev-text="<i class='bi bi-chevron-left'></i>"
        next-text="<i class='bi bi-chevron-right'></i>"
        :page-range="perPage"
        :click-handler="setPage"
      />
    </div>
  </template>

  <!-- If no comments -->
  <div class="row" v-else>
    <div class="col">
      <p>No comments yet</p>
    </div>
  </div>
</template>

<script>
import UserAvatar from '@/components/UserAvatar.vue'
import Paginate from 'vuejs-paginate-next'

export default {
  name: 'CommentContainer',
  components: {
    UserAvatar,
    Paginate
  },
  props: ['postId'],
  async mounted() {
    if (!this.postId) {
      return
    }

    const comments_res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/posts/${this.postId}/comments`)
    this.comments = await comments_res.json()

    var users_in_comments = this.comments.map(comment => comment.authorId)
    this.users = []
    users_in_comments.forEach(async userId => {
      const user_res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/users/${userId}`)
      this.users.push(await user_res.json())
    })
  },
  data () {
    return {
      users: [],
      comments: [],
      perPage: 3,
      currentPage: 1
    }
  },
  methods: {
    async addComment() {
      const input = this.$refs['comment-input']
      if (input.value) {
        var comment = {
          postId: this.postId,
          authorId: this.$store.state.user.id,
          content: input.value
        }
        const res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/api/posts/${this.postId}/comments`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(comment)
        })
        if (res.ok) {
          this.comments.unshift(comment)
          if (!this.users.find(user => user.id == comment.authorId)) {
            this.users.push(this.$store.state.user)
          }
          input.value = ''
        } else {
          alert('Failed to add comment')
        }
      }
    },
    setPage(pageNum) {
      this.currentPage = pageNum
    }
  },
  computed: {
    pageCount() {
      return Math.ceil(this.comments.length / this.perPage)
    },
    paginatedComments() {
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
      return this.comments.slice(start, end)
    }
  },
}
</script>

<style scoped>
.comment-input {
  background-color: #D9D9D9;
  border-radius: 24px;
  transition: 0.5s;
}
.comment-input * {
  height: 30px;
  font-size: 14px;
  background-color: transparent;
  border: none;
  border-radius: 24px;
}
.comment-input:not(.disabled):hover {
  background-color: #BFBFBF;
  transition: 0.5s;
}
.comment-input:not(.disabled):focus-within {
  background-color: #f0f0f0;
  transition: 0.5s;
}
.comment-input.disabled {
  background-color: #f0f0f0;
}
.comment-name {
  font-weight: 600;
  font-size: 14px;
}
.comment-content {
  font-weight: 400;
  font-size: 14px;
}
</style>