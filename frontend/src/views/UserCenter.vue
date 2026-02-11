<template>
  <div class="user-center-container">
    <h1>个人中心</h1>
    
    <el-row :gutter="20">
      <!-- 左侧导航菜单 -->
      <el-col :span="6">
        <el-menu
          :default-active="activeMenu"
          class="user-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="profile">
            <i class="el-icon-user"></i>
            <span>个人资料</span>
          </el-menu-item>
          <el-menu-item index="favorites">
            <i class="el-icon-star-on"></i>
            <span>我的收藏</span>
          </el-menu-item>
          <el-menu-item index="comments">
            <i class="el-icon-chat-dot-round"></i>
            <span>我的评论</span>
          </el-menu-item>
          <el-menu-item index="browse-history">
            <i class="el-icon-time"></i>
            <span>浏览记录</span>
          </el-menu-item>
          <el-menu-item index="click-behavior">
            <i class="el-icon-mouse"></i>
            <span>点击行为</span>
          </el-menu-item>
        </el-menu>
      </el-col>
      
      <!-- 右侧内容区域 -->
      <el-col :span="18">
        <el-card class="content-card">
          <!-- 个人资料 -->
          <div v-if="activeMenu === 'profile'">
            <div class="section-header">
              <h2>个人资料</h2>
              <el-button type="primary" @click="$router.push('/user')">修改资料</el-button>
            </div>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="用户名">{{ userProfile.username }}</el-descriptions-item>
              <el-descriptions-item label="昵称">{{ userProfile.nickname }}</el-descriptions-item>
              <el-descriptions-item label="邮箱">{{ userProfile.email }}</el-descriptions-item>
              <el-descriptions-item label="手机号">{{ userProfile.phone }}</el-descriptions-item>
              <el-descriptions-item label="性别">{{ userProfile.gender }}</el-descriptions-item>
              <el-descriptions-item label="城市">{{ userProfile.city }}</el-descriptions-item>
              <el-descriptions-item label="出生日期">{{ userProfile.birth_date }}</el-descriptions-item>
              <el-descriptions-item label="注册时间">{{ userProfile.created_at }}</el-descriptions-item>
            </el-descriptions>
          </div>
          
          <!-- 我的收藏 -->
          <div v-else-if="activeMenu === 'favorites'">
            <div class="section-header">
              <h2>我的收藏 ({{ favorites.length }})</h2>
            </div>
            <el-table :data="favorites" style="width: 100%">
              <el-table-column prop="house_id" label="房屋ID" width="180"></el-table-column>
              <el-table-column prop="favorited_at" label="收藏时间" width="180"></el-table-column>
              <el-table-column label="状态" width="100">
                <template slot-scope="scope">
                  <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                    {{ scope.row.is_active ? '已收藏' : '已取消' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button 
                    v-if="scope.row.is_active"
                    size="mini" 
                    type="danger" 
                    @click="cancelFavorite(scope.row)"
                  >
                    取消收藏
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          
          <!-- 我的评论 -->
          <div v-else-if="activeMenu === 'comments'">
            <div class="section-header">
              <h2>我的评论 ({{ comments.length }})</h2>
            </div>
            <el-table :data="comments" style="width: 100%">
              <el-table-column prop="house_id" label="房屋ID" width="180"></el-table-column>
              <el-table-column prop="comment" label="评论内容"></el-table-column>
              <el-table-column prop="rating" label="评分" width="100">
                <template slot-scope="scope">
                  <el-rate
                    v-if="scope.row.rating"
                    v-model="scope.row.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                  ></el-rate>
                  <span v-else>无评分</span>
                </template>
              </el-table-column>
              <el-table-column prop="commented_at" label="评论时间" width="180"></el-table-column>
            </el-table>
          </div>
          
          <!-- 浏览记录 -->
          <div v-else-if="activeMenu === 'browse-history'">
            <div class="section-header">
              <h2>浏览记录 ({{ browseHistory.length }})</h2>
            </div>
            <el-table :data="browseHistory" style="width: 100%">
              <el-table-column prop="house_id" label="房屋ID" width="180"></el-table-column>
              <el-table-column prop="viewed_at" label="浏览时间" width="180"></el-table-column>
              <el-table-column prop="duration" label="浏览时长(秒)" width="120"></el-table-column>
              <el-table-column prop="session_id" label="会话ID"></el-table-column>
            </el-table>
          </div>
          
          <!-- 点击行为 -->
          <div v-else-if="activeMenu === 'click-behavior'">
            <div class="section-header">
              <h2>点击行为 ({{ clickBehaviors.length }})</h2>
            </div>
            <el-table :data="clickBehaviors" style="width: 100%">
              <el-table-column prop="house_id" label="房屋ID" width="180"></el-table-column>
              <el-table-column prop="clicked_at" label="点击时间" width="180"></el-table-column>
              <el-table-column prop="session_id" label="会话ID"></el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'UserCenter',
  data() {
    return {
      activeMenu: 'profile',
      userProfile: {},
      favorites: [],
      comments: [],
      browseHistory: [],
      clickBehaviors: []
    }
  },
  async mounted() {
    if (!this.isAuthenticated()) {
      this.$message.warning('请先登录')
      this.$router.push('/login')
      return
    }
    await this.loadUserData()
  },
  methods: {
    handleMenuSelect(key) {
      this.activeMenu = key
    },
    
    async loadUserData() {
      try {
        // 加载用户基本信息
        const userInfo = localStorage.getItem('userInfo')
        if (userInfo) {
          this.userProfile = JSON.parse(userInfo)
        }
        
        // 加载收藏数据
        const favResponse = await this.$http.get('/api/user/favorites/')
        if (favResponse.data.success) {
          this.favorites = favResponse.data.data
        }
        
        // 加载评论数据
        const commentResponse = await this.$http.get('/api/user/comments/')
        if (commentResponse.data.success) {
          this.comments = commentResponse.data.data
        }
        
        // 加载浏览记录
        const historyResponse = await this.$http.get('/api/user/browse-history/')
        if (historyResponse.data.success) {
          this.browseHistory = historyResponse.data.data
        }
        
        // 加载点击行为
        const clickResponse = await this.$http.get('/api/user/click-behaviors/')
        if (clickResponse.data.success) {
          this.clickBehaviors = clickResponse.data.data
        }
        
      } catch (error) {
        console.error('加载用户数据失败:', error)
        this.$message.error('数据加载失败')
      }
    },
    
    async cancelFavorite(row) {
      try {
        const response = await this.$http.post('/api/houses/toggle-favorite/', {
          house_id: row.house_id
        })
        
        if (response.data.success) {
          row.is_active = false
          this.$message.success('取消收藏成功')
        } else {
          this.$message.error(response.data.message)
        }
      } catch (error) {
        console.error('取消收藏失败:', error)
        this.$message.error('操作失败')
      }
    },
    
    isAuthenticated() {
      return localStorage.getItem('isAuthenticated') === 'true'
    }
  }
}
</script>

<style scoped>
.user-center-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.user-center-container h1 {
  color: #333;
  margin-bottom: 20px;
}

.user-menu {
  border-radius: 8px;
  overflow: hidden;
}

.user-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
}

.user-menu .el-menu-item i {
  margin-right: 10px;
  color: #667eea;
}

.content-card {
  min-height: 500px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.section-header h2 {
  margin: 0;
  color: #333;
}
</style>