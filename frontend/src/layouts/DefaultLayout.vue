<template>
  <div class="default-layout">
    <HeaderBar />
    <router-view/>
  </div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar.vue'

export default {
  name: 'DefaultLayout',
  components: {
    HeaderBar
  }
}
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
}
</style>