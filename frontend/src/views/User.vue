<template>
  <div class="user">
    <h1>用户中心</h1>
    <div v-if="user">

    </div>
    <div v-else>
      <p>请登录</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'User',
  computed: {
    user() {
      return this.$store.state.user
    }
  }
}
</script>