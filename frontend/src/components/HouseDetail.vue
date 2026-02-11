<template>
  <el-dialog
    :visible.sync="dialogVisible"
    :title="house.building_name"
    width="80%"
    class="house-detail-dialog"
    @close="$emit('close')"
    :modal-append-to-body="false"
    :append-to-body="true"
  >
    <div class="house-detail-container">
      <el-scrollbar style="height: 600px;">
        <div class="detail-content">
          <!-- 收藏区域 -->
          <div class="favorite-section">
            <div class="floating-favorite" @click="toggleFavorite">
              <i :class="house.is_favorite ? 'el-icon-star-on' : 'el-icon-star-off'"></i>
              <span>{{ house.is_favorite ? '已收藏' : '收藏' }}</span>
            </div>
          </div>
          
          <!-- 房屋基本信息 -->
          <div class="basic-info-section">
            <h2 class="house-title">{{ house.building_name }}</h2>
            
            <div class="price-section">
              <div class="main-price">
                <span class="price-number">¥{{ formatPrice(house.price) }}</span>
                <span class="price-unit">/月</span>
              </div>
              <div class="price-tags">
                <el-tag v-if="house.method" :type="getMethodTagType(house.method)">{{ house.method }}</el-tag>
              </div>
            </div>
            
            <div class="house-meta">
              <div class="meta-item">
                <i class="el-icon-location-information"></i>
                <span>{{ house.city }} · {{ house.city_district }} · {{ house.district_area }}</span>
              </div>
              <div class="meta-item">
                <i class="el-icon-house"></i>
                <span>{{ house.area_sqm }}㎡</span>
              </div>
              <div class="meta-item">
                <i class="el-icon-sunny"></i>
                <span>{{ house.orientation }}</span>
              </div>
              <div class="meta-item">
                <i class="el-icon-sort"></i>
                <span>{{ house.floor_type }} {{ house.floor_number }}层</span>
              </div>
            </div>
            
            <div class="room-type-tags">
              <el-tag v-if="house.room_type" type="success" size="medium">{{ house.room_type }}</el-tag>
              <el-tag v-for="tag in formatTags(house.tags)" :key="tag" size="medium">{{ tag }}</el-tag>
            </div>
          </div>
          
          <!-- 详细信息表格 -->
          <el-card class="detail-card">
            <div slot="header" class="card-header">
              <span>房屋详细信息</span>
            </div>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="城市">{{ house.city }}</el-descriptions-item>
              <el-descriptions-item label="出租方式">{{ house.method }}</el-descriptions-item>
              <el-descriptions-item label="楼盘名称">{{ house.building_name }}</el-descriptions-item>
              <el-descriptions-item label="户型">{{ house.room_type }}</el-descriptions-item>
              <el-descriptions-item label="城市地区">{{ house.city_district }}</el-descriptions-item>
              <el-descriptions-item label="区内地段">{{ house.district_area }}</el-descriptions-item>
              <el-descriptions-item label="建筑面积">{{ house.area_sqm }}㎡</el-descriptions-item>
              <el-descriptions-item label="朝向">{{ house.orientation }}</el-descriptions-item>
              <el-descriptions-item label="楼层类型">{{ house.floor_type }}</el-descriptions-item>
              <el-descriptions-item label="楼层">{{ house.floor_number }}</el-descriptions-item>
              <el-descriptions-item label="标签" :span="2">
                <el-tag v-for="tag in formatTags(house.tags)" :key="tag" style="margin-right: 5px;">{{ tag }}</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
          
          <!-- 外部链接 -->
          <el-card class="link-card" v-if="house.detail_link">
            <div slot="header" class="card-header">
              <span>查看详情</span>
            </div>
            <div class="external-link">
              <el-button type="primary" @click="openExternalLink">
                <i class="el-icon-link"></i>
                查看原始房源信息
              </el-button>
              <p class="link-note">点击将跳转到链家网查看完整房源信息</p>
            </div>
          </el-card>
          
          <!-- 评论区域 -->
          <el-card class="comments-card">
            <div slot="header" class="card-header">
              <span>用户评论</span>
              <el-button 
                v-if="isAuthenticated()" 
                type="primary" 
                size="small" 
                @click="showCommentDialog = true"
                style="float: right;"
              >
                发表评论
              </el-button>
            </div>
            
            <!-- 评论列表 -->
            <div v-if="comments.length > 0" class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment-item">
                <div class="comment-header">
                  <span class="comment-user">{{ comment.user.nickname || comment.user.username }}</span>
                  <span class="comment-time">{{ comment.commented_at }}</span>
                  <el-rate
                    v-if="comment.rating"
                    v-model="comment.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}分"
                    style="display: inline-block; margin-left: 10px;"
                  ></el-rate>
                </div>
                <div class="comment-content">{{ comment.comment }}</div>
              </div>
            </div>
            <div v-else class="no-comments">
              <i class="el-icon-chat-dot-round"></i>
              <p>暂无评论，快来发表第一条评论吧！</p>
            </div>
          </el-card>
        </div>
      </el-scrollbar>
      
      <!-- 发表评论对话框 -->
      <el-dialog
        title="发表评论"
        :visible.sync="showCommentDialog"
        width="500px"
        @close="resetCommentForm"
        :modal-append-to-body="false"
        :append-to-body="true"
      >
        <el-form :model="commentForm" :rules="commentRules" ref="commentForm" label-width="80px">
          <el-form-item label="评分" prop="rating">
            <el-rate
              v-model="commentForm.rating"
              show-score
              text-color="#ff9900"
              score-template="{value}分"
            ></el-rate>
          </el-form-item>
          <el-form-item label="评论内容" prop="comment">
            <el-input
              type="textarea"
              :rows="4"
              placeholder="请输入您的评论..."
              v-model="commentForm.comment"
              maxlength="500"
              show-word-limit
            ></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="showCommentDialog = false">取 消</el-button>
          <el-button type="primary" @click="submitComment" :loading="commentLoading">发 表</el-button>
        </div>
      </el-dialog>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'HouseDetail',
  props: {
    house: {
      type: Object,
      required: true
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      comments: [],
      showCommentDialog: false,
      commentLoading: false,
      commentForm: {
        rating: null,
        comment: ''
      },
      commentRules: {
        comment: [
          { required: true, message: '请输入评论内容', trigger: 'blur' },
          { min: 1, max: 500, message: '长度在 1 到 500 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    dialogVisible: {
      get() {
        return this.visible;
      },
      set() {
        this.$emit('close');
      }
    }
  },
  async mounted() {
    await this.loadComments()
  },
  methods: {
    async loadComments() {
      try {
        const response = await this.$http.get(`/api/houses/comments/${this.house.house_id}/`)
        if (response.data.success) {
          this.comments = response.data.data
        }
      } catch (error) {
        console.error('加载评论失败:', error)
      }
    },
    
    async toggleFavorite() {
      if (!this.isAuthenticated()) {
        this.$message.warning('请先登录')
        this.$router.push('/login')
        return
      }
      
      try {
        const response = await this.$http.post('/api/houses/toggle-favorite/', {
          house_id: this.house.house_id
        })
        
        if (response.data.success) {
          this.house.is_favorite = response.data.data.is_favorite
          this.$message.success(response.data.message)
        } else {
          this.$message.error(response.data.message)
        }
      } catch (error) {
        console.error('切换收藏状态失败:', error)
        this.$message.error('操作失败')
      }
    },
    
    openExternalLink() {
      if (this.house.detail_link) {
        window.open(this.house.detail_link, '_blank')
      }
    },
    
    async submitComment() {
      if (!this.isAuthenticated()) {
        this.$message.warning('请先登录')
        this.$router.push('/login')
        return
      }
      
      this.$refs.commentForm.validate(async (valid) => {
        if (valid) {
          this.commentLoading = true
          try {
            const response = await this.$http.post(`/api/houses/add-comment/${this.house.house_id}/`, {
              comment: this.commentForm.comment,
              rating: this.commentForm.rating
            })
            
            if (response.data.success) {
              this.comments.unshift(response.data.data)
              this.$message.success('评论发表成功')
              this.showCommentDialog = false
              this.resetCommentForm()
            } else {
              this.$message.error(response.data.message)
            }
          } catch (error) {
            console.error('发表评论失败:', error)
            this.$message.error('发表评论失败')
          } finally {
            this.commentLoading = false
          }
        }
      })
    },
    
    resetCommentForm() {
      this.commentForm = {
        rating: null,
        comment: ''
      }
      this.$refs.commentForm && this.$refs.commentForm.resetFields()
    },
    
    formatTags(tags) {
      if (!tags || tags === '未知') return []
      return tags.split('、').filter(tag => tag.trim())
    },
    
    formatPrice(price) {
      if (!price) return '0'
      return parseFloat(price).toLocaleString()
    },
    
    getMethodTagType(method) {
      const typeMap = {
        '整租': 'primary',
        '合租': 'success'
      }
      return typeMap[method] || 'info'
    },
    
    isAuthenticated() {
      return localStorage.getItem('isAuthenticated') === 'true'
    }
  }
}
</script>

<style scoped>
.house-detail-container {
  padding: 20px;
}

.detail-content {
  max-width: 1200px;
  margin: 0 auto;
}

.favorite-section {
  position: relative;
  margin-bottom: 30px;
}

.floating-favorite {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px 15px;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  z-index: 10;
}

.floating-favorite:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.floating-favorite i {
  font-size: 18px;
  color: #ffd700;
}

.basic-info-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.house-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 20px 0;
  color: #333;
}

.price-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.main-price {
  display: flex;
  align-items: baseline;
}

.price-number {
  font-size: 32px;
  font-weight: bold;
  color: #ff6b6b;
}

.price-unit {
  font-size: 16px;
  color: #666;
  margin-left: 5px;
}

.house-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #666;
}

.meta-item i {
  margin-right: 8px;
  color: #409EFF;
  font-size: 16px;
}

.room-type-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.detail-card, .link-card, .comments-card {
  margin-bottom: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.external-link {
  text-align: center;
  padding: 20px;
}

.link-note {
  color: #909399;
  font-size: 12px;
  margin-top: 10px;
}

.comments-list {
  max-height: 400px;
  overflow-y: auto;
}

.comment-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.comment-user {
  font-weight: bold;
  color: #409EFF;
  margin-right: 15px;
}

.comment-time {
  color: #909399;
  font-size: 12px;
}

.comment-content {
  color: #333;
  line-height: 1.6;
  padding-left: 10px;
}

.no-comments {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
}

.no-comments i {
  font-size: 48px;
  margin-bottom: 10px;
  display: block;
}

.dialog-footer {
  text-align: right;
}

/* 对话框样式 */
.house-detail-dialog >>> .el-dialog {
  border-radius: 8px;
}

.house-detail-dialog >>> .el-dialog__header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 8px 8px 0 0;
}

.house-detail-dialog >>> .el-dialog__title {
  color: white;
  font-size: 18px;
  font-weight: bold;
}

.house-detail-dialog >>> .el-dialog__body {
  padding: 0;
}

/* 滚动条样式 */
.el-scrollbar >>> .el-scrollbar__wrap {
  overflow-x: hidden;
}

.el-scrollbar >>> .el-scrollbar__bar.is-vertical {
  width: 6px;
}

.el-scrollbar >>> .el-scrollbar__thumb {
  background-color: rgba(144, 147, 153, 0.3);
  border-radius: 3px;
}
</style>