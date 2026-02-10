<template>
  <div class="auth-layout">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout'
}
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
}
</style>