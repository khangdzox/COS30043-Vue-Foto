<template>
  <div class="position-relative overflow-hidden">
    <!-- Left edge button -->
    <div class="to-left edge-button d-flex align-items-center position-absolute top-50 start-0 translate-middle-y" @click="scrollLeft()" v-if="shouldShowLeft">
      <i class="bi bi-chevron-left"></i>
    </div>

    <!-- List content -->
    <div class="d-flex flex-nowrap justify-content-start horizontal-scroll" ref="horizontal-scroll">
      <slot></slot>
    </div>

    <!-- Right edge button -->
    <div class="to-right edge-button d-flex align-items-center position-absolute top-50 end-0 translate-middle-y" @click="scrollRight()" v-if="shouldShowRight">
      <i class="bi bi-chevron-right"></i>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HorizontalList',
  props: {
    parentBgColor: {
      type: String,
      default: '#f5f5f5'
    }
  },
  data () {
    return {
      shouldShowLeft: false,
      shouldShowRight: false
    }
  },
  mounted () {
    // Initial check for edge buttons
    this.$nextTick( this.checkShowArrows() )

    // Check for edge buttons on scroll and resize
    this.$refs['horizontal-scroll'].addEventListener('scroll', this.checkShowArrows)
    window.addEventListener('resize', this.checkShowArrows)
  },
  unmounted () {
    this.$refs['horizontal-scroll']?.removeEventListener('scroll', this.checkShowArrows)
    window.removeEventListener('resize', this.checkShowArrows)
  },
  updated () {
    // Check for edge buttons on slot update
    this.checkShowArrows()
  },
  methods: {
    scrollLeft() {
      this.$refs['horizontal-scroll'].scrollBy({
        left: -200,
        behavior: 'smooth'
      });
    },
    scrollRight() {
      this.$refs['horizontal-scroll'].scrollBy({
        left: 200,
        behavior: 'smooth'
      });
    },
    checkShowArrows() {
      this.shouldShowLeft = this.checkShowLeft()
      this.shouldShowRight = this.checkShowRight()
    },
    checkShowLeft() {
      return this.$refs['horizontal-scroll'].scrollLeft > 0;
    },
    checkShowRight() {
      return this.$refs['horizontal-scroll'].scrollLeft < this.$refs['horizontal-scroll'].scrollWidth - this.$refs['horizontal-scroll'].clientWidth;
    }
  }
}
</script>

<style scoped>
.edge-button {
  height: 100%;
  cursor: pointer;
  font-size: 20px;
}
.to-left {
  padding-right: 30px;
  background: linear-gradient(to left, v-bind(parentBgColor + '00'), v-bind(parentBgColor + 'ff'), v-bind(parentBgColor + 'ff'));
}
.to-right {
  padding-left: 30px;
  background: linear-gradient(to right, v-bind(parentBgColor + '00'), v-bind(parentBgColor + 'ff'), v-bind(parentBgColor + 'ff'));
}
.horizontal-scroll {
  width: 100%;
  height: 100%;
  overflow-x: scroll;
  gap: 10px;
}
.horizontal-scroll::-webkit-scrollbar {
  display: none;
}
</style>