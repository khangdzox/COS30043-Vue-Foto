<template>
  <div class="row px-1 pb-3 m-3 gy-3 post-form">
    <div class="col-12 col-lg-6">
      <img class="w-100 h-auto post-img-prv" v-if="imgsrc != ''" :src="imgsrc" alt="Post Image">
      <div class="w-100 h-100 position-relative post-img-placeholder" v-else>
        <i class="bi bi-image position-absolute top-50 start-50 translate-middle post-img-placeholder-icon"></i>
      </div>
    </div>
    <div class="col-12 col-lg-6">
      <form novalidate @submit.prevent="submitPost" @reset.prevent="discardChanges">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input type="text" class="form-control" id="title" name="title" v-model="title">
          <div class="invalid-feedback fw-bold d-block">
            {{ formValidateMsg.title }}
          </div>
        </div>
        <div class="mb-3">
          <label for="imgsrc" class="form-label">Image URL</label>
          <input type="url" class="form-control" id="imgsrc" name="imgsrc" v-model="imgsrc">
          <div class="invalid-feedback fw-bold d-block">
            {{ formValidateMsg.imgsrc }}
          </div>
        </div>
        <div class="mb-3">
          <label for="desc" class="form-label">Description</label>
          <textarea class="form-control" id="desc" name="desc" v-model="desc" @input="(event) => event.target.style.height = event.target.scrollHeight + 'px'"></textarea>
        </div>
        <div class="mb-3">
          <label for="tags" class="form-label">Tags</label>
          <div id="tags-help" class="form-text">Enter comma-separated list of tags.</div>
          <input type="text" class="form-control" id="tags" name="tags" v-model="tags">
          <HorizontalList class="mt-3" v-if="tagsList.length > 0">
            <TagPill v-for="tag in tagsList" :key="tag" :font-size="14">
              {{ tag }}
            </TagPill>
          </HorizontalList>
        </div>
        <div class="mb-3 d-flex flex-wrap gap-3">
          <button v-if="isEdit" type="button" class="btn btn-danger" @click="deletePost">
            <i class="bi bi-trash-fill"></i>&nbsp;
            Delete
          </button>
          <button type="reset" class="btn btn-secondary">
            <i class="bi bi-arrow-counterclockwise"></i>&nbsp;
            Discard
          </button>
          <button type="submit" class="btn btn-primary">
            <i class="bi bi-check2"></i>&nbsp;
            Submit
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import HorizontalList from '@/components/HorizontalList.vue';
import TagPill from '@/components/TagPill.vue';

export default {
  name: 'PostEditView',
  components: {
    HorizontalList,
    TagPill
  },
  async created() {
    if (!this.$store.state.user) {
      this.$router.push('/login')
      return
    }

    if (this.$route.params.postId) {
      const post_res = await fetch(`/api/posts/${this.$route.params.postId}`)
      const post = await post_res.json()

      if (this.$store.state.user.id != post.authorId) {
        this.$router.push(`/post/${post.id}`)
        return
      }

      this.imgsrc = post.img;
      this.tags = post.tags ? post.tags : '';
      this.title = post.title;
      this.desc = post.content;
      this.isEdit = true;
    }
  },
  data() {
    return {
      imgsrc: '',
      tags: '',
      title: '',
      desc: '',
      isEdit: false,
      resetText: 'Discard',
      submitText: '',
      formValidateMsg: {
        imgsrc: '',
        title: ''
      }
    }
  },
  computed: {
    tagsList() {
      return this.tags.split(',').map(tag => tag.trim());
    }
  },
  methods: {
    async submitPost() {

      if (this.title === '') {
        this.formValidateMsg.title = 'Title is required';
      } else {
        this.formValidateMsg.title = '';
      }

      if (this.imgsrc === '') {
        this.formValidateMsg.imgsrc = 'Image URL is required';
      } else {
        this.formValidateMsg.imgsrc = '';
      }

      if (!(
        this.formValidateMsg.title === '' &&
        this.formValidateMsg.imgsrc === ''
      )) {
        return;
      }

      if (!confirm('Are you sure you want to submit this post?')) return;

      if (this.isEdit) {
        const res = await fetch(`/api/posts/${this.$route.params.postId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            authorId: this.$store.state.user.id,
            title: this.title,
            posted: new Date().toISOString().split('T')[0],
            img: this.imgsrc,
            content: this.desc,
            tags: this.tagsList
          })
        })
        if (res.ok) {
          this.$router.push(`/post/${this.$route.params.postId}`)
        } else {
          alert('Failed to update post')
        }
      } else {
        const res = await fetch(`/api/posts`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            authorId: this.$store.state.user.id,
            title: this.title,
            posted: new Date().toISOString().split('T')[0],
            img: this.imgsrc,
            content: this.desc,
            tags: this.tagsList
          })
        })
        if (res.ok) {
          const post = await res.json()
          this.$router.push(`/post/${post.id}`)
        } else {
          alert('Failed to add post')
        }
      }
    },
    discardChanges() {
      if (!confirm('Are you sure you want to discard changes?')) return;
      if (this.isEdit) {
        this.$router.push(`/post/${this.$route.params.postId}`)
      } else {
        this.imgsrc = '';
        this.tags = '';
        this.title = '';
        this.desc = '';
      }
    },
    deletePost() {
      if (!confirm('Are you sure you want to delete this post?')) return;
      fetch(`/api/posts/${this.$route.params.postId}`, {
        method: 'DELETE'
      })
    }
  }
}
</script>

<style scoped>
.post-form {
  background-color: #fff;
  border-radius: 30px;
  box-shadow: 20px 20px 60px #d9d9d9, -20px -20px 60px #ffffff;
}
.post-img-prv {
  border-radius: 24px;
}
.post-img-placeholder {
  background: linear-gradient(135deg, #D9D9D9 0%, #F5F5F5 59.5%, #FFFFFF 100%);
  border-radius: 24px;
}
.post-img-placeholder-icon {
  font-size: 60px;
  color: #6c757d;
}
</style>