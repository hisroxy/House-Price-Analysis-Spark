<template>
  <div class="header-bar">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="0" @click="goToDashboard">
        <span class="logo">🏠 房价分析系统</span>
      </el-menu-item>
      <el-menu-item index="1">首页</el-menu-item>
      <el-menu-item index="2">房源管理</el-menu-item>
      <el-menu-item index="3">智能推荐</el-menu-item>
      <el-menu-item index="4">用户中心</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'HeaderBar',
  data() {
    return {
      activeIndex: '1'
    }
  },
  methods: {
    goToDashboard() {
      this.$router.push('/')
    },
    handleSelect(key) {
      switch(key) {
        case '1':
          this.$router.push('/home')
          break
        case '2':
          this.$router.push('/houses')
          break
        case '3':
          this.$router.push('/recommend')
          break
        case '4':
          this.$router.push('/user')
          break
      }
    }
  }
}
</script>

<style scoped>
.header-bar {
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
}

.logo {
  font-weight: bold;
  font-size: 18px;
}
</style>