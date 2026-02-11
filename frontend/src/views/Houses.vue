<template>
  <div class="houses-container">
    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <div slot="header" class="search-header">
        <span>房屋搜索</span>
      </div>
      
      <el-form :model="searchForm" label-width="80px" class="search-form">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="城市">
              <el-select v-model="searchForm.city" placeholder="请选择城市" clearable>
                <el-option label="深圳" value="深圳"></el-option>
                <el-option label="广州" value="广州"></el-option>
                <el-option label="佛山" value="佛山"></el-option>
                <el-option label="东莞" value="东莞"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="6">
            <el-form-item label="区域">
              <el-input v-model="searchForm.city_district" placeholder="请输入区域" clearable></el-input>
            </el-form-item>
          </el-col>
          
          <el-col :span="6">
            <el-form-item label="户型">
              <el-select v-model="searchForm.room_type" placeholder="请选择户型" clearable>
                <el-option label="1室0厅" value="1室0厅"></el-option>
                <el-option label="1室1厅" value="1室1厅"></el-option>
                <el-option label="2室1厅" value="2室1厅"></el-option>
                <el-option label="2室2厅" value="2室2厅"></el-option>
                <el-option label="3室1厅" value="3室1厅"></el-option>
                <el-option label="3室2厅" value="3室2厅"></el-option>
                <el-option label="4室2厅" value="4室2厅"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="6">
            <el-form-item label="朝向">
              <el-select v-model="searchForm.orientation" placeholder="请选择朝向" clearable>
                <el-option label="东" value="东"></el-option>
                <el-option label="南" value="南"></el-option>
                <el-option label="西" value="西"></el-option>
                <el-option label="北" value="北"></el-option>
                <el-option label="东南" value="东南"></el-option>
                <el-option label="东北" value="东北"></el-option>
                <el-option label="西南" value="西南"></el-option>
                <el-option label="西北" value="西北"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="价格范围">
              <el-col :span="11">
                <el-input-number v-model="searchForm.min_price" :min="0" placeholder="最低价" style="width: 100%"></el-input-number>
              </el-col>
              <el-col class="line" :span="2" style="text-align: center">-</el-col>
              <el-col :span="11">
                <el-input-number v-model="searchForm.max_price" :min="0" placeholder="最高价" style="width: 100%"></el-input-number>
              </el-col>
            </el-form-item>
          </el-col>
          
          <el-col :span="8">
            <el-form-item label="面积范围">
              <el-col :span="11">
                <el-input-number v-model="searchForm.min_area" :min="0" placeholder="最小面积" style="width: 100%"></el-input-number>
              </el-col>
              <el-col class="line" :span="2" style="text-align: center">-</el-col>
              <el-col :span="11">
                <el-input-number v-model="searchForm.max_area" :min="0" placeholder="最大面积" style="width: 100%"></el-input-number>
              </el-col>
            </el-form-item>
          </el-col>
          
          <el-col :span="8">
            <el-form-item label="标签搜索">
              <el-input v-model="searchForm.tags" placeholder="输入标签关键词" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="24" style="text-align: right;">
            <el-button type="primary" @click="searchHouses" :loading="loading">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    
    <!-- 排序和结果统计 -->
    <div class="result-header">
      <div class="result-info">
        共找到 <span class="total-count">{{ pagination.total }}</span> 套房源
      </div>
      <div class="sort-options">
        <span>排序：</span>
        <el-select v-model="sort.field" @change="handleSortChange" size="small">
          <el-option label="价格升序" value="price_asc"></el-option>
          <el-option label="价格降序" value="price_desc"></el-option>
          <el-option label="面积升序" value="area_sqm_asc"></el-option>
          <el-option label="面积降序" value="area_sqm_desc"></el-option>
        </el-select>
      </div>
    </div>
    
    <!-- 房屋列表 -->
    <div class="houses-grid">
      <el-card 
        v-for="(house, index) in houses" 
        :key="`${house.house_id}_${index}`" 
        class="house-card"
        @click.native="viewHouseDetail(house)"
      >
        <div class="house-content">
          <!-- 收藏按钮 -->
          <div class="favorite-btn" @click.stop="toggleFavorite(house)">
            <i :class="house.is_favorite ? 'el-icon-star-on' : 'el-icon-star-off'"></i>
          </div>
          
          <!-- 房屋基本信息 -->
          <div class="house-info">
            <h3 class="house-title">{{ house.building_name }}</h3>
            <div class="house-tags">
              <el-tag size="mini" v-if="house.method">{{ house.method }}</el-tag>
              <el-tag size="mini" type="success" v-if="house.room_type">{{ house.room_type }}</el-tag>
              <el-tag size="mini" type="warning" v-if="house.orientation">{{ house.orientation }}</el-tag>
              <el-tag size="mini" type="info" v-for="tag in formatTags(house.tags)" :key="tag">{{ tag }}</el-tag>
            </div>
            
            <div class="house-details">
              <div class="detail-item">
                <i class="el-icon-location-outline"></i>
                <span>{{ house.city }} {{ house.city_district }} {{ house.district_area }}</span>
              </div>
              <div class="detail-item">
                <i class="el-icon-house"></i>
                <span>{{ house.area_sqm }}㎡</span>
              </div>
              <div class="detail-item">
                <i class="el-icon-sort"></i>
                <span>{{ house.floor_type }} {{ house.floor_number }}层</span>
              </div>
            </div>
            
            <div class="house-price">
              <span class="price-number">¥{{ formatPrice(house.price) }}</span>
              <span class="price-unit">/月</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-sizes="[12, 24, 36, 48]"
        :page-size="pagination.page_size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total">
      </el-pagination>
    </div>
    
    <!-- 房屋详情对话框 -->
    <house-detail 
      v-if="dialogVisible" 
      :house="currentHouse"
      :visible="dialogVisible"
      @close="dialogVisible = false"
    ></house-detail>
  </div>
</template>

<script>
import HouseDetail from '@/components/HouseDetail.vue'

export default {
  name: 'Houses',
  components: {
    HouseDetail
  },
  data() {
    return {
      loading: false,
      houses: [],
      searchForm: {
        city: '',
        city_district: '',
        room_type: '',
        orientation: '',
        min_price: null,
        max_price: null,
        min_area: null,
        max_area: null,
        tags: ''
      },
      sort: {
        field: 'price_asc'
      },
      pagination: {
        page: 1,
        page_size: 12,
        total: 0,
        total_pages: 0
      },
      dialogVisible: false,
      currentHouse: {}
    }
  },
  async mounted() {
    await this.loadHouses()
  },
  methods: {
    async loadHouses() {
      this.loading = true
      try {
        const params = new URLSearchParams()
        params.append('page', this.pagination.page)
        params.append('page_size', this.pagination.page_size)
        
        // 添加搜索条件
        Object.keys(this.searchForm).forEach(key => {
          const value = this.searchForm[key];
          if (value !== '' && value !== null && value !== undefined) {
            // 数值类型参数只在大于0时添加
            if (['min_price', 'max_price', 'min_area', 'max_area'].includes(key)) {
              if (parseFloat(value) > 0) {
                params.append(key, value);
              }
            } else {
              params.append(key, value);
            }
          }
        })
        
        // 添加排序
        const [field, order] = this.sort.field.split('_')
        params.append('sort_field', field)
        params.append('sort_order', order)
        
        // 调试日志
        console.log('请求参数:', params.toString())
        
        const response = await this.$http.get(`/api/houses/list/?${params.toString()}`)
        
        if (response.data.success) {
          this.houses = response.data.data.data
          this.pagination.total = response.data.data.total
          this.pagination.total_pages = response.data.data.total_pages
        } else {
          this.$message.error(response.data.message || '获取房屋列表失败')
        }
      } catch (error) {
        console.error('获取房屋列表失败:', error)
        this.$message.error('网络请求失败')
      } finally {
        this.loading = false
      }
    },
    
    searchHouses() {
      this.pagination.page = 1
      this.loadHouses()
    },
    
    resetSearch() {
      this.searchForm = {
        city: '',
        city_district: '',
        room_type: '',
        orientation: '',
        min_price: null,
        max_price: null,
        min_area: null,
        max_area: null,
        tags: ''
      }
      this.pagination.page = 1
      this.loadHouses()
    },
    
    handleSortChange() {
      this.loadHouses()
    },
    
    handleSizeChange(val) {
      this.pagination.page_size = val
      this.pagination.page = 1
      this.loadHouses()
    },
    
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadHouses()
    },
    
    async toggleFavorite(house) {
      if (!this.isAuthenticated()) {
        this.$message.warning('请先登录')
        this.$router.push('/login')
        return
      }
      
      try {
        const response = await this.$http.post('/api/houses/toggle-favorite/', {
          house_id: house.house_id
        })
        
        if (response.data.success) {
          house.is_favorite = response.data.data.is_favorite
          this.$message.success(response.data.message)
        } else {
          this.$message.error(response.data.message)
        }
      } catch (error) {
        console.error('切换收藏状态失败:', error)
        this.$message.error('操作失败')
      }
    },
    
    viewHouseDetail(house) {
      this.currentHouse = house
      this.dialogVisible = true
    },
    
    formatTags(tags) {
      if (!tags || tags === '未知') return []
      return tags.split('、').filter(tag => tag.trim())
    },
    
    formatPrice(price) {
      if (!price) return '0'
      return parseFloat(price).toLocaleString()
    },
    
    isAuthenticated() {
      return localStorage.getItem('isAuthenticated') === 'true'
    }
  }
}
</script>

<style scoped>
.houses-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.search-card {
  margin-bottom: 20px;
}

.search-header {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.search-form >>> .el-form-item {
  margin-bottom: 15px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px 20px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.result-info {
  font-size: 16px;
  color: #666;
}

.total-count {
  color: #409EFF;
  font-weight: bold;
  font-size: 18px;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 10px;
}

.houses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.house-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.house-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.house-content {
  position: relative;
}

.favorite-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.favorite-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.1);
}

.favorite-btn i {
  font-size: 18px;
  color: #ffd700;
}

.house-info {
  padding: 15px;
}

.house-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 10px 0;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.house-tags {
  margin-bottom: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.house-details {
  margin-bottom: 15px;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
  font-size: 13px;
  color: #666;
}

.detail-item i {
  margin-right: 5px;
  color: #409EFF;
}

.house-price {
  display: flex;
  align-items: baseline;
}

.price-number {
  font-size: 20px;
  font-weight: bold;
  color: #ff6b6b;
}

.price-unit {
  font-size: 14px;
  color: #666;
  margin-left: 5px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
</style>