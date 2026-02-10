<template>
  <div class="header-bar">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#ffffff"
      text-color="#333"
      active-text-color="#667eea"
    >
      <el-menu-item index="0" @click="goToDashboard">
        <span class="logo">🏠 房价分析系统</span>
      </el-menu-item>

      <el-menu-item index="1">首页</el-menu-item>
      <el-menu-item index="2">房源管理</el-menu-item>
      <el-menu-item index="3">智能推荐</el-menu-item>
      
      <!-- 用户区域 - 右对齐 -->
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
      activeIndex: '1',
      isAuthenticated: false,
      userInfo: {
        nickname: '',
        avatar: ''
      }
    }
  },
  computed: {
    userAvatar() {
      return this.userInfo.avatar || '/default-avatar.png'
    }
  },
  mounted() {
    this.checkAuthStatus()
  },
  methods: {
    goToDashboard() {
      this.$router.push('/')
      this.activeIndex = '0'
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
        '/user': '4'
      }
      this.activeIndex = routeMap[to.path] || '1'
    }
  }
}
</script>

<style scoped>
.header-bar {
  box-shadow: 0 2px 12px rgba(0,0,0,.1);
  background: white;
}

.el-menu-demo {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  font-weight: bold;
  font-size: 20px;
  color: #667eea !important;
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
  padding: 8px 12px;
  border-radius: 20px;
  transition: background-color 0.3s ease;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 8px;
  object-fit: cover;
  border: 2px solid #e1e5e9;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  margin-right: 4px;
  color: #333;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

.auth-btn {
  font-size: 14px;
  padding: 8px 16px;
}

.register-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.register-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .el-menu-demo {
    padding: 0 10px;
  }
  
  .logo {
    font-size: 16px;
  }
  
  .user-name {
    display: none;
  }
  
  .auth-buttons {
    gap: 5px;
  }
  
  .auth-btn {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>