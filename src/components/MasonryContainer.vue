<template>
  <div class="masonry container">
    <div class="row">
      <div class="col"></div>
      <div class="col" v-if="columns >= 2"></div>
      <div class="col" v-if="columns >= 3"></div>
      <div class="col" v-if="columns >= 4"></div>
      <div class="col" v-if="columns >= 5"></div>
      <div class="col" v-if="columns >= 6"></div>

      <div ref="masonry_img_temp">
        <slot :arrange="arrange"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MasonryContainer',
  props: {
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
      type: Number,
      default: 10
    }
  },
  mounted () {
    this.children = [...this.$refs.masonry_img_temp.children]
    this.width = this.$el.querySelector('.row').offsetWidth
    this.columns = this.computeColumns()

    for (const child of this.children) {
      child.style.marginBottom = `${this.gap}px`
    }

    window.addEventListener('resize', this.onResize)
  },
  updated () {
    this.arrange()
  },
  unmounted () {
    window.removeEventListener('resize', this.onResize)
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
        return
      }

      this.width = width
      this.columns = this.computeColumns()

      this.arrange()
    },

    arrange () {
      let colIndex = 0
      let imgIndex = 0

      const cols = this.$el.querySelectorAll('.col')
      for (const col of cols) {
        col.innerHTML = ''
      }

      const colHeights = Array.from(cols).fill(0)

      while (imgIndex < this.children.length) {
        const elem = this.children[imgIndex]

        cols[colIndex].appendChild(elem)
        colHeights[colIndex] += parseInt(elem.offsetHeight) + parseInt(this.gap)

        imgIndex++
        colIndex = colHeights.indexOf(Math.min(...colHeights))
      }
    },

    computeColumns () {
      let columns = 1
      if (this.width >= 1320) {
        columns = this.xxl
      } else if (this.width >= 1140) {
        columns = this.xl
      } else if (this.width >= 960) {
        columns = this.lg
      } else if (this.width >= 720) {
        columns = this.md
      } else {
        columns = this.sm
      }
      return columns
    }
  }
}
</script>
