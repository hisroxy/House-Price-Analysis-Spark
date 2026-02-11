<template>
  <div class="header-bar">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#ffffff"
      text-color="#333333"
      active-text-color="#667eea"
    >
      <div class="logo" @click="goToDashboard">
        <i class="el-icon-office-building logo-icon"></i>
        <span class="logo-text">房价分析系统</span>
      </div>
      
      <!-- 导航菜单 -->
      <div class="nav-menu-container">
        <el-menu-item index="1" class="nav-item">首页</el-menu-item>
        <el-menu-item index="2" class="nav-item">房屋分析</el-menu-item>
        <el-menu-item index="3" class="nav-item">智能推荐</el-menu-item>
        <el-menu-item index="4" class="nav-item">敬请期待</el-menu-item>
        <el-menu-item index="5" v-if="isAuthenticated" class="nav-item">个人中心</el-menu-item>
      </div>
      
      <div class="user-section">
        <template v-if="isAuthenticated">
          <!-- 已登录状态 -->
          <el-dropdown @command="handleUserCommand" trigger="click">
            <div class="user-info">
              <img 
                :src="userAvatar" 
                :alt="userInfo.nickname" 
                class="user-avatar"
              />
              <span class="user-name">{{ userInfo.nickname }}</span>
              <i class="el-icon-arrow-down el-icon--right"></i>
            </div>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="settings">设置</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
        <template v-else>
          <!-- 未登录状态 -->
          <div class="auth-buttons">
            <el-button 
              type="text" 
              @click="$router.push('/login')"
              class="auth-btn"
            >
              登录
            </el-button>
            <el-button 
              type="primary" 
              @click="$router.push('/register')"
              class="auth-btn register-btn"
            >
              注册
            </el-button>
          </div>
        </template>
      </div>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'HeaderBar',
  data() {
    return {
      activeIndex: '0',
      isAuthenticated: false,
      userInfo: {
        nickname: '',
        avatar: ''
      }
    }
  },
  computed: {
    userAvatar() {
      return this.userInfo.avatar || 'https://ss2.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1659552792,3869332496&fm=253&gp=0.jpg'
    }
  },
  mounted() {
    this.checkAuthStatus()
    // 初始化时根据当前路由设置激活菜单项
    this.$nextTick(() => {
      const routeMap = {
        '/': '0',
        '/home': '1',
        '/houses': '2',
        '/recommend': '3',
        '/user': '5'
      }
      // 大屏页面不显示激活状态
      this.activeIndex = (this.$route.path === '/') ? '' : (routeMap[this.$route.path] || '1')
    })
  },
  methods: {
    goToDashboard() {
      this.$router.push('/')
      this.activeIndex = ''
    },

    handleSelect(key) {
      this.activeIndex = key
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
          this.$message.info('敬请期待更多功能上线')
          break
        case '5':
          this.$router.push('/user-center')
          break
      }
    },
    
    checkAuthStatus() {
      // 检查本地存储中的认证状态
      const authStatus = localStorage.getItem('isAuthenticated')
      const userInfo = localStorage.getItem('userInfo')
      
      if (authStatus === 'true' && userInfo) {
        this.isAuthenticated = true
        this.userInfo = JSON.parse(userInfo)
      }
    },
    
    async handleUserCommand(command) {
      switch(command) {
        case 'profile':
          this.$router.push('/user')
          break
        case 'settings':
          this.$message.info('设置功能开发中')
          break
        case 'logout':
          await this.handleLogout()
          break
      }
    },
    
    async handleLogout() {
      try {
        const response = await fetch('/api/user/logout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        
        const data = await response.json()
        
        if (data.success) {
          // 清除本地存储
          localStorage.removeItem('isAuthenticated')
          localStorage.removeItem('userInfo')
          
          this.isAuthenticated = false
          this.userInfo = {}
          
          this.$message.success('退出登录成功')
          this.$router.push('/login')
        } else {
          this.$message.error(data.message || '退出登录失败')
        }
      } catch (error) {
        console.error('退出登录错误:', error)
        // 即使服务器请求失败，也清除本地状态
        localStorage.removeItem('isAuthenticated')
        localStorage.removeItem('userInfo')
        this.isAuthenticated = false
        this.userInfo = {}
        this.$router.push('/login')
      }
    }
  },
  watch: {
    // 监听路由变化，同步激活菜单项
    '$route'(to) {
      const routeMap = {
        '/': '0',
        '/home': '1',
        '/houses': '2',
        '/recommend': '3',
        '/user': '5',
        '/user-center': '5'
      }
      // 大屏页面不显示激活状态
      this.activeIndex = (to.path === '/') ? '' : (routeMap[to.path] || '1')
    }
  }
}
</script>

<style scoped>
.header-bar {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background: linear-gradient(to right, #ffffff, #fafbff);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #eef1f6;
}

.el-menu-demo {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  height: 70px;
  border: none !important;
}

.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 10px 15px;
  border-radius: 12px;
}

.logo:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.logo-icon {
  font-size: 24px;
  color: #667eea;
  margin-right: 10px;
  transition: all 0.3s ease;
}

.logo:hover .logo-icon {
  transform: rotate(10deg) scale(1.1);
  color: #764ba2;
}

.logo-text {
  font-weight: 700;
  font-size: 22px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu-container {
  display: flex;
  align-items: center;
  height: 100%;
}

.nav-item {
  height: 50px !important;
  line-height: 50px !important;
  min-width: 100px !important;
  text-align: center;
  margin: 0 5px;
  border-radius: 10px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative;
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
  transition: left 0.5s;
}

.nav-item:hover::before {
  left: 100%;
}

.nav-item:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2) !important;
  color: #667eea !important;
}

.nav-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
  font-weight: 600 !important;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
  transform: translateY(-2px) !important;
}

.user-section {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 10px 16px;
  border-radius: 25px;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border: 1px solid #e1e8ff;
}

.user-info:hover {
  background: linear-gradient(135deg, #eff2ff 0%, #e6eeff 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(102, 126, 234, 0.2);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
  border: 2px solid #667eea;
  transition: all 0.3s ease;
}

.user-info:hover .user-avatar {
  transform: scale(1.1);
  border-color: #764ba2;
}

.user-name {
  font-size: 15px;
  font-weight: 600;
  margin-right: 6px;
  color: #333;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
}

.auth-btn {
  font-size: 15px;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.auth-btn:not(.register-btn) {
  color: #667eea;
  background: transparent;
  border-color: #667eea;
}

.auth-btn:not(.register-btn):hover {
  background: #667eea;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.register-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.register-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .el-menu-demo {
    padding: 0 20px;
  }
  
  .nav-item {
    min-width: 90px !important;
    font-size: 14px;
  }
}

@media (max-width: 992px) {
  .el-menu-demo {
    padding: 0 15px;
  }
  
  .logo-text {
    font-size: 18px;
  }
  
  .nav-item {
    min-width: 80px !important;
    font-size: 13px;
    margin: 0 3px;
  }
  
  .user-name {
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .el-menu-demo {
    padding: 0 10px;
    height: 60px;
  }
  
  .logo {
    padding: 8px 12px;
  }
  
  .logo-icon {
    font-size: 20px;
    margin-right: 8px;
  }
  
  .logo-text {
    font-size: 16px;
  }
  
  .nav-item {
    min-width: 70px !important;
    height: 40px !important;
    line-height: 40px !important;
    font-size: 12px;
    margin: 0 2px;
  }
  
  .user-info {
    padding: 8px 12px;
  }
  
  .user-avatar {
    width: 30px;
    height: 30px;
  }
  
  .user-name {
    display: none;
  }
  
  .auth-buttons {
    gap: 8px;
  }
  
  .auth-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
}

@media (max-width: 576px) {
  .el-menu-demo {
    padding: 0 8px;
  }
  
  .logo-text {
    display: none;
  }
  
  .nav-item {
    min-width: 60px !important;
    font-size: 11px;
  }
  
  .auth-btn:not(.register-btn) {
    padding: 6px 12px;
    font-size: 12px;
  }
  
  .register-btn {
    padding: 8px 16px;
    font-size: 12px;
  }
}
</style>