<template>
  <!-- Comment textbox -->
  <div class="row">
    <form class="col" @submit.prevent="addComment()">

      <div v-if="this.$store.state.user" class="input-group comment-input">
        <input type="text" class="form-control" placeholder="Comment here..." ref="comment-input">
        <button class="btn" type="submit">
          <i class="bi bi-send"></i>
        </button>
      </div>

      <div v-else class="input-group comment-input disabled">
        <input type="text" class="form-control" placeholder="You must login to comment" ref="comment-input" disabled>
      </div>
    </form>
  </div>

  <!-- Comments -->
  <template v-if="comments.length > 0">
    <div class="row g-2" v-for="comment in comments" :key="comment">
      <div class="col-auto">
        <UserAvatar :userId="comment.authorId" :size="32"/>
      </div>
      <div class="col">
        <div class="comment-name">{{ users.find(user => user.id == comment.authorId).name }}</div>
        <div class="comment-content">{{ comment.content }}</div>
      </div>
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
import Users from '@/assets/users.json'
import Comments from '@/assets/comments.json'
import UserAvatar from '@/components/UserAvatar.vue'

export default {
  name: 'CommentContainer',
  components: {
    UserAvatar
  },
  props: ['postId'],
  data () {
    return {
      users: Users,
      comments: Comments.filter(comment => comment.postId == this.postId)
    }
  },
  methods: {
    addComment() {
      const input = this.$refs['comment-input']
      if (input.value) {
        this.comments.push({
          authorId: this.$store.state.user.id,
          postId: this.postId,
          content: input.value
        })
        input.value = ''
      }
    }
  }
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