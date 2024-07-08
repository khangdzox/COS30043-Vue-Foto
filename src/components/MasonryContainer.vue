<template>
  <div class="mt-3">
    <div class="row">
      <!-- Predefine 6 columns to move contents in -->
      <div class="col"></div>
      <div class="col" v-if="columns >= 2"></div>
      <div class="col" v-if="columns >= 3"></div>
      <div class="col" v-if="columns >= 4"></div>
      <div class="col" v-if="columns >= 5"></div>
      <div class="col" v-if="columns >= 6"></div>

      <!-- Main content slot -->
      <div ref="masonry_img_temp">
        <template v-for="post in posts" :key="post.id">
          <PostThumbnail :post="post" @image-loaded="arrange"/>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import PostThumbnail from '@/components/PostThumbnail.vue'

export default {
  name: 'MasonryContainer',
  props: {
    posts: {
      type: Array,
      default: () => []
    },
    sm: {
      type: Number,
      default: 1
    },
    md: {
      type: Number,
      default: 2
    },
    lg: {
      type: Number,
      default: 3
    },
    xl: {
      type: Number,
      default: 4
    },
    xxl: {
      type: Number,
      default: 6
    },
    gap: {
      type: String,
      default: '10'
    }
  },
  components: {
    PostThumbnail,
  },
  mounted () {
    this.children = [...this.$refs.masonry_img_temp.children]   // Get all children
    this.width = this.$el.querySelector('.row').offsetWidth     // Get the width of the layout
    this.columns = this.computeColumns()                        // Compute the number of columns

    window.onresize = this.onResize                             // Add resize event listener
  },
  updated () {
    if (this.$refs.masonry_img_temp.children.length > 0) {
      this.children = [...this.$refs.masonry_img_temp.children] // Update children
    }

    this.arrange()                                              // Rearrange images when updated
  },
  unmounted () {
    window.onresize = null                                      // Remove resize event listener
  },
  data () {
    return {
      width: 1,
      columns: 1,
      children: []
    }
  },
  methods: {
    onResize () {
      const width = this.$el.querySelector('.row').offsetWidth

      if (width === this.width) {
        // Only rearrange if the width has changed to prevent unnecessary calls
        return
      }

      this.width = width
      this.columns = this.computeColumns()

      this.arrange()
    },

    arrange () {
      let colIndex = 0
      let imgIndex = 0

      const cols = this.$el.querySelectorAll('.col')                                  // Clear all columns
      for (const col of cols) {
        col.innerHTML = ''
      }

      const colHeights = Array.from(cols).fill(0)                                     // Initialize column heights

      while (imgIndex < this.children.length) {
        const elem = this.children[imgIndex]
        elem.style.marginBottom = `${this.gap}px`                                    // Set the gap between images

        cols[colIndex].appendChild(elem)                                              // Append image to column
        colHeights[colIndex] += parseInt(elem.offsetHeight) + parseInt(this.gap)      // Update column height

        imgIndex++                                                                    // Move to next image
        colIndex = colHeights.indexOf(Math.min(...colHeights))                        // Find the shortest column to append next image
      }
    },

    computeColumns () {
      let columns = 1
      if (this.width >= 1296) {
        columns = this.xxl
      } else if (this.width >= 1116) {
        columns = this.xl
      } else if (this.width >= 936) {
        columns = this.lg
      } else if (this.width >= 696) {
        columns = this.md
      } else {
        columns = this.sm
      }
      return columns
    }
  }
}
</script>
