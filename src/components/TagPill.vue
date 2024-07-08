<template>
  <span class="badge rounded-pill tag-pill text-capitalize">
    <slot></slot>
  </span>
</template>

<script>
export default {
  name: 'TagPill',
  props: ["fontSize"]
}
</script>

<style>
.tag-pill {
  padding: v-bind(0.5 * parseInt(fontSize) + 'px') v-bind(fontSize + 'px') !important;
  background-color: #eee;
  transition: background-color 0.3s;
}
.tag-pill:hover {
  background-color: #ccc;
  transition: background-color 0.3s;
}
.tag-pill,
.tag-pill * {
  font-size: v-bind(fontSize + 'px') !important;
  font-weight: 600 !important;
  color: #000000 !important;
  text-decoration: none;
}
</style>
