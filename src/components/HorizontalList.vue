<template>
  <div class="position-relative overflow-hidden">
    <div class="to-left edge-button d-flex align-items-center position-absolute top-50 start-0 translate-middle-y" @click="scrollLeft()" v-if="shouldShowLeft">
      <i class="bi bi-chevron-left"></i>
    </div>
    <div class="d-flex flex-nowrap justify-content-start horizontal-scroll" ref="horizontal-scroll">
      <slot></slot>
    </div>
    <div class="to-right edge-button d-flex align-items-center position-absolute top-50 end-0 translate-middle-y" @click="scrollRight()" v-if="shouldShowRight">
      <i class="bi bi-chevron-right"></i>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HorizontalList',
  data() {
    return {
      shouldShowLeft: false,
      shouldShowRight: false
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.shouldShowLeft = this.checkShowLeft();
      this.shouldShowRight = this.checkShowRight();
    });
    this.$refs['horizontal-scroll'].addEventListener('scroll', () => {
      this.shouldShowLeft = this.checkShowLeft();
      this.shouldShowRight = this.checkShowRight();
    });
    window.addEventListener('resize', () => {
      this.shouldShowLeft = this.checkShowLeft();
      this.shouldShowRight = this.checkShowRight();
    });
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
  background: linear-gradient(to left, #f5f5f500, #f5f5f5ff, #f5f5f5ff);
}
.to-right {
  padding-left: 30px;
  background: linear-gradient(to right, #f5f5f500, #f5f5f5ff, #f5f5f5ff);
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