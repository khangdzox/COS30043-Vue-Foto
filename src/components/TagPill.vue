<template>
  <span class="badge rounded-pill tag-pill">
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
  text-transform: capitalize;
  background-color: #eee;
  transition: background-color 0.3s;
}
.tag-pill:hover {
  background-color: #ccc;
  transition: background-color 0.3s;
}
.tag-pill a {
  font-size: v-bind(fontSize + 'px');
  font-weight: 600;
  color: #000000;
  text-decoration: none;
}
</style>
