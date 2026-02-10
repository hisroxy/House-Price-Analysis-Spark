<template>
  <div class="user-container">
    <h1>个人信息</h1>
    <p>修改您的个人资料</p>
    
    <!-- 头像预览区域 -->
    <div class="avatar-preview-section">
      <div class="avatar-preview-box">
        <img 
          :src="formData.avatar || 'https://ss2.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1659552792,3869332496&fm=253&gp=0.jpg'" 
          :alt="formData.nickname || formData.username" 
          class="avatar-image"
          @error="handleAvatarError"
        />
        <div class="avatar-info">
          <p class="avatar-text">头像预览</p>
          <p class="avatar-desc">支持外部图片链接</p>
        </div>
      </div>
    </div>
    
    <el-form :model="formData" ref="userForm" label-width="100px" class="user-form">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="formData.username" disabled />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="formData.email" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="formData.phone" />
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-select v-model="formData.gender">
              <el-option label="男" value="男"></el-option>
              <el-option label="女" value="女"></el-option>
              <el-option label="未知" value="未知"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        
        <el-col :span="12">
          <el-form-item label="昵称" prop="nickname">
            <el-input v-model="formData.nickname" />
          </el-form-item>
          <el-form-item label="城市" prop="city">
            <el-input v-model="formData.city" />
          </el-form-item>
          <el-form-item label="头像URL" prop="avatar">
            <el-input 
              v-model="formData.avatar" 
              placeholder="请输入图片URL地址"
              @input="handleAvatarInput"
            >
              <template #append>
                <el-button @click="loadAvatarPreview" :loading="avatarLoading">加载</el-button>
              </template>
            </el-input>
            <div v-if="avatarPreviewUrl" class="avatar-preview-result">
              <img 
                :src="avatarPreviewUrl" 
                alt="头像预览" 
                class="preview-image"
                @error="handlePreviewError"
                @load="handlePreviewLoad"
              />
              <span class="preview-status success" v-if="previewLoaded">✓ 预览成功</span>
              <span class="preview-status error" v-else-if="previewError">✗ 加载失败</span>
              <span class="preview-status loading" v-else>加载中...</span>
            </div>
          </el-form-item>
          <el-form-item label="出生日期" prop="birth_date">
            <el-date-picker v-model="formData.birth_date" type="date" value-format="yyyy-MM-dd" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <div class="form-actions">
        <el-button type="primary" @click="saveUserInfo" :loading="loading">保存修改</el-button>
        <el-button @click="resetForm">重置</el-button>
        <el-button @click="$router.push('/')">返回</el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'User',
  data() {
    return {
      formData: {
        username: '',
        email: '',
        phone: '',
        gender: '未知',
        nickname: '',
        city: '',
        avatar: '',
        birth_date: ''
      },
      loading: false,
      user: {},
      avatarPreviewUrl: '',
      avatarLoading: false,
      previewLoaded: false,
      previewError: false
    }
  },
  async mounted() {
    await this.loadUserInfo()
  },
  methods: {
    async loadUserInfo() {
      try {
        const userInfo = localStorage.getItem('userInfo')
        if (userInfo) {
          this.user = JSON.parse(userInfo)
          this.formData = {
            username: this.user.username || '',
            email: this.user.email || '',
            phone: this.user.phone || '',
            gender: this.user.gender || '未知',
            nickname: this.user.nickname || '',
            city: this.user.city || '',
            avatar: this.user.avatar || '',
            birth_date: this.user.birth_date || ''
          }
        } else {
          const response = await this.$http.get('/api/user/user-info/')
          if (response.data.success) {
            this.user = response.data.data
            this.formData = {
              username: this.user.username || '',
              email: this.user.email || '',
              phone: this.user.phone || '',
              gender: this.user.gender || '未知',
              nickname: this.user.nickname || '',
              city: this.user.city || '',
              avatar: this.user.avatar || '',
              birth_date: this.user.birth_date || ''
            }
          }
        }
        // 初始化头像预览
        if (this.formData.avatar) {
          this.avatarPreviewUrl = this.formData.avatar
          this.loadAvatarPreview()
        }
      } catch (error) {
        console.error('加载用户信息失败:', error)
        this.$message.error('加载用户信息失败')
      }
    },
    
    handleAvatarInput(value) {
      // 输入时实时更新预览URL
      this.avatarPreviewUrl = value
      this.previewLoaded = false
      this.previewError = false
      
      // 如果有内容，自动尝试加载
      if (value && value.trim()) {
        this.debounceLoadPreview()
      }
    },
    
    debounceLoadPreview() {
      // 防抖处理，避免频繁请求
      clearTimeout(this.previewTimer)
      this.previewTimer = setTimeout(() => {
        this.loadAvatarPreview()
      }, 500)
    },
    
    async loadAvatarPreview() {
      if (!this.formData.avatar || !this.formData.avatar.trim()) {
        this.avatarPreviewUrl = ''
        this.previewLoaded = false
        this.previewError = false
        return
      }
      
      this.avatarLoading = true
      this.previewError = false
      
      try {
        // 创建一个测试图片来验证URL是否有效
        const img = new Image()
        img.onload = () => {
          this.previewLoaded = true
          this.avatarLoading = false
          this.previewError = false
          this.$message.success('头像预览加载成功')
        }
        img.onerror = () => {
          this.previewError = true
          this.avatarLoading = false
          this.previewLoaded = false
          this.$message.error('头像URL无效或无法访问')
        }
        img.src = this.formData.avatar
      } catch (error) {
        this.previewError = true
        this.avatarLoading = false
        this.previewLoaded = false
        this.$message.error('头像加载失败')
      }
    },
    
    handlePreviewLoad() {
      this.previewLoaded = true
      this.previewError = false
    },
    
    handlePreviewError() {
      this.previewError = true
      this.previewLoaded = false
    },
    
    handleAvatarError(event) {
      // 头像加载失败时显示默认头像
      event.target.src = 'https://ss2.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1659552792,3869332496&fm=253&gp=0.jpg'

      this.$message.warning('头像加载失败，已使用默认头像')
    },
    
    async saveUserInfo() {
      this.loading = true
      try {
        const response = await this.$http.put('/api/user/update-info/', {
          email: this.formData.email,
          phone: this.formData.phone,
          gender: this.formData.gender,
          nickname: this.formData.nickname,
          city: this.formData.city,
          avatar: this.formData.avatar,
          birth_date: this.formData.birth_date
        })
        
        if (response.data.success) {
          this.$message.success('保存成功！')
          
          // 更新localStorage
          const updatedUser = { ...this.user, ...this.formData }
          localStorage.setItem('userInfo', JSON.stringify(updatedUser))
          this.user = updatedUser
        } else {
          this.$message.error(response.data.message || '保存失败')
        }
      } catch (error) {
        console.error('保存失败:', error)
        this.$message.error('网络错误，请稍后重试')
      } finally {
        this.loading = false
      }
    },
    
    resetForm() {
      this.formData = {
        username: this.user.username || '',
        email: this.user.email || '',
        phone: this.user.phone || '',
        gender: this.user.gender || '未知',
        nickname: this.user.nickname || '',
        city: this.user.city || '',
        avatar: this.user.avatar || '',
        birth_date: this.user.birth_date || ''
      }
    }
  }
}
</script>

<style scoped>
.user-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.user-container h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 8px;
}

.user-container p {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}

.avatar-preview-section {
  margin-bottom: 24px;
}

.avatar-preview-box {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #f5f7fa;
  border-radius: 12px;
  padding: 20px;
}

.avatar-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e1e5e9;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.avatar-info {
  text-align: left;
}

.avatar-text {
  color: #333;
  font-weight: 500;
  margin-bottom: 4px;
}

.avatar-desc {
  color: #666;
  font-size: 12px;
}

.avatar-preview-result {
  margin-top: 10px;
  text-align: center;
}

.preview-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e1e5e9;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  margin-bottom: 8px;
}

.preview-status {
  font-size: 12px;
  font-weight: 500;
}

.preview-status.success {
  color: #67c23a;
}

.preview-status.error {
  color: #f56c6c;
}

.preview-status.loading {
  color: #409eff;
}

.user-form {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.form-actions {
  margin-top: 20px;
}
</style>