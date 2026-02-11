<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  color: #2c3e50;
  background: #f8fafc;
  min-height: 100vh;
}

/* 全局过渡动画 */
.page-enter-active, .page-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter, .page-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 字体优化 */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: #f8fafc;
  color: #333;
}

/* 链接样式 */
a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: #764ba2;
}

/* 选择文本样式 */
::selection {
  background: rgba(102, 126, 234, 0.3);
  color: #333;
}
</style>