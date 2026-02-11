<template>
  <div class="dashboard dark-theme">
    <!-- 顶部概览卡片：显示房源总数、平均价格、最高价格、最低价格 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="(stat, index) in overviewStats" :key="index">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number" :style="{ color: stat.color }">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 第一行：地图和数据表格 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <!-- 地理分布地图卡片 -->
        <el-card class="chart-card map-card">
          <div slot="header" class="chart-header">广东省房源地理分布</div>
          <div ref="mapChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <!-- 详细数据表格卡片 -->
        <el-card class="chart-card table-card">
          <div slot="header" class="chart-header">详细数据表格</div>
          <el-table :data="tableData" height="400" stripe class="dark-table">
            <el-table-column prop="city" label="城市" width="100"></el-table-column>
            <el-table-column prop="avg_price" label="均价" width="120">
              <template slot-scope="scope">¥{{ scope.row.avg_price }}</template>
            </el-table-column>
            <el-table-column prop="house_count" label="房源数" width="100"></el-table-column>
            <el-table-column prop="max_price" label="最高价" width="120">
              <template slot-scope="scope">¥{{ scope.row.max_price }}</template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    

    
    <!-- 第二行：区域分布、户型统计和均价排行 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="8">
        <!-- 区域房源分布饼图 -->
        <el-card class="chart-card mini-card">
          <div slot="header" class="chart-header">区域房源分布</div>
          <div ref="areaChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <!-- 户型统计分析柱状图 -->
        <el-card class="chart-card mini-card">
          <div slot="header" class="chart-header">户型统计分析</div>
          <div ref="roomTypeChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <!-- 城市均价排行柱状图 -->
        <el-card class="chart-card mini-card">
          <div slot="header" class="chart-header">城市均价排行</div>
          <div ref="priceTrendChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 第三行：朝向分布、价格区间和词云图 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="8">
        <!-- 房源朝向分布饼图 -->
        <el-card class="chart-card mini-card">
          <div slot="header" class="chart-header">房源朝向分布</div>
          <div ref="orientationChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <!-- 价格区间分布条形图 -->
        <el-card class="chart-card mini-card">
          <div slot="header" class="chart-header">价格区间分布</div>
          <div ref="priceRangeChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <!-- 房源标签词云图 -->
        <el-card class="chart-card mini-card">
          <div slot="header" class="chart-header">房源标签词云</div>
          <div ref="wordCloudChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
    

    
    <!-- 加载提示：数据加载时显示遮罩层 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>数据加载中...</p>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import guangdongJson from '@/assets/Guangdong.json'

export default {
  name: 'Dashboard',
  data() {
    return {
      loading: false,  // 控制加载状态显示
      dashboardData: {},  // 存储从后端获取的dashboard数据
      charts: {}  // 存储ECharts实例
    }
  },
  computed: {
    // 计算顶部统计卡片数据
    overviewStats() {
      const data = this.dashboardData.overview || {}
      return [
        { label: '房源总数', value: (data.total_houses || 0).toLocaleString(), color: '#409EFF' },
        { label: '平均价格', value: `¥${(data.avg_price || 0).toLocaleString()}`, color: '#67C23A' },
        { label: '最高价格', value: `¥${(data.max_price || 0).toLocaleString()}`, color: '#E6A23C' },
        { label: '最低价格', value: `¥${(data.min_price || 0).toLocaleString()}`, color: '#F56C6C' }
      ]
    },
    // 计算表格数据来源
    tableData() {
      return this.dashboardData.price_trend || []
    }
  },
  async mounted() {
    await this.loadData()
    this.$nextTick(() => {
      this.initCharts()
    })
  },
  beforeDestroy() {
    this.disposeCharts()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const response = await this.$http.get('/api/dashboard/data/')
        if (response.data.success) {
          this.dashboardData = response.data.data
        } else {
          // Hive查询失败，显示错误信息
          console.error('Hive数据查询失败:', response.data.message)
          this.dashboardData = {}
          this.showError('数据加载失败，请检查Hive服务是否正常运行')
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        this.dashboardData = {}
        this.showError('网络请求失败，请检查后端服务是否正常运行')
      } finally {
        this.loading = false
      }
    },
    
    showError(message) {
      this.$message({
        message: message,
        type: 'error'
      })
    },
    
    initCharts() {
      // 只有当有数据时才初始化图表
      if (!this.dashboardData || Object.keys(this.dashboardData).length === 0) {
        return
      }
      this.initMapChart()
      this.initPriceTrendChart()
      this.initAreaChart()
      this.initRoomTypeChart()
      this.initOrientationChart()
      this.initPriceRangeChart()
      this.initWordCloudChart()
    },
    initMapChart() {
      const chartDom = this.$refs.mapChart
      if (!chartDom) return
      
      this.charts.map = echarts.init(chartDom)
      echarts.registerMap('guangdong', guangdongJson)
      
      const option = {
        tooltip: { trigger: 'item', formatter: '{b}<br/>房源数量: {c}' },
        visualMap: {
          min: 0, max: 5000, left: 'left', top: 'bottom',
          text: ['高', '低'], calculable: true,
          inRange: { color: ['#50a3ba', '#eac736', '#d94e5d'] }
        },
        series: [{
          name: '房源数量', type: 'map', map: 'guangdong',
          data: this.dashboardData.area_distribution || []
        }]
      }
      this.charts.map.setOption(option)
    },
    initPriceTrendChart() {
      const chartDom = this.$refs.priceTrendChart
      if (!chartDom) return
      
      this.charts.priceTrend = echarts.init(chartDom)
      const data = this.dashboardData.price_trend || []
      
      const option = {
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: data.map(item => item.city) },
        yAxis: { type: 'value', axisLabel: { formatter: '¥{value}' } },
        series: [{
          name: '均价', type: 'bar',
          data: data.map(item => item.avg_price),
          itemStyle: { color: '#409EFF' }
        }]
      }
      this.charts.priceTrend.setOption(option)
    },
    initAreaChart() {
      const chartDom = this.$refs.areaChart
      if (!chartDom) return
      
      this.charts.area = echarts.init(chartDom)
      const data = this.dashboardData.area_distribution || []
      
      const option = {
        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
        series: [{
          name: '区域分布', type: 'pie', radius: ['40%', '70%'],
          data: data.slice(0, 8)
        }]
      }
      this.charts.area.setOption(option)
    },
    initRoomTypeChart() {
      const chartDom = this.$refs.roomTypeChart
      if (!chartDom) return
      
      this.charts.roomType = echarts.init(chartDom)
      const data = this.dashboardData.room_type_stats || []
      
      const option = {
        tooltip: { trigger: 'axis' },
        legend: { data: ['房源数量', '平均价格'] },
        xAxis: { type: 'category', data: data.map(item => item.room_type) },
        yAxis: [
          { type: 'value', name: '数量' },
          { type: 'value', name: '价格', axisLabel: { formatter: '¥{value}' } }
        ],
        series: [
          { name: '房源数量', type: 'bar', data: data.map(item => item.count) },
          { name: '平均价格', type: 'line', yAxisIndex: 1, data: data.map(item => item.avg_price) }
        ]
      }
      this.charts.roomType.setOption(option)
    },
    initOrientationChart() {
      const chartDom = this.$refs.orientationChart
      if (!chartDom) return
      
      this.charts.orientation = echarts.init(chartDom)
      const data = this.dashboardData.orientation_stats || []
      
      const option = {
        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
        series: [{
          name: '朝向分布', type: 'pie', radius: '60%',
          data: data
        }]
      }
      this.charts.orientation.setOption(option)
    },
    initPriceRangeChart() {
      const chartDom = this.$refs.priceRangeChart
      if (!chartDom) return
      
      this.charts.priceRange = echarts.init(chartDom)
      const data = this.dashboardData.price_range_distribution || []
      
      const option = {
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'value' },
        yAxis: { type: 'category', data: data.map(item => item.range) },
        series: [{
          name: '房源数量', type: 'bar',
          data: data.map(item => item.count),
          itemStyle: { color: '#E6A23C' }
        }]
      }
      this.charts.priceRange.setOption(option)
    },
    initWordCloudChart() {
      const chartDom = this.$refs.wordCloudChart
      if (!chartDom) return
      
      this.charts.wordCloud = echarts.init(chartDom)
      const data = this.dashboardData.tags_wordcloud || []
      
      const option = {
        tooltip: { show: true },
        series: [{
          type: 'wordCloud', gridSize: 8, sizeRange: [12, 50],
          rotationRange: [-90, 90], shape: 'pentagon',
          textStyle: {
            color: function() {
              return 'rgb(' + [Math.round(Math.random() * 160), Math.round(Math.random() * 160), Math.round(Math.random() * 160)].join(',') + ')'
            }
          },
          data: data
        }]
      }
      this.charts.wordCloud.setOption(option)
    },
    disposeCharts() {
      Object.values(this.charts).forEach(chart => chart && chart.dispose())
      this.charts = {}
    }
  }
}
</script>

<style scoped>
/* 整体页面样式 */
.dark-theme {
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  color: #e0e0e0;
  min-height: 90vh;
  padding: 50px;  /* 两侧留白40px */
  font-family: 'Consolas', 'Monaco', monospace;
}

/* 顶部统计卡片行样式 */
.stats-row {
  margin-bottom: 15px;
}

/* 顶部统计卡片样式 */
.stat-card {
  background: rgba(30, 30, 46, 0.8);
  border: 1px solid rgba(79, 172, 254, 0.3);
  border-radius: 4px;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 20px rgba(79, 172, 254, 0.2);
  height: 100px;  /* 符合规范：顶部统计卡100px */
  transition: all 0.3s ease;
}

/* 统计卡片悬停效果 */
.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 30px rgba(79, 172, 254, 0.4);
  border-color: rgba(79, 172, 254, 0.6);
}

/* 统计卡片内边距 */
.stat-card ::v-deep .el-card__body {
  padding: 20px;
}

/* 统计内容居中 */
.stat-content {
  text-align: center;
}

/* 统计数字样式 */
.stat-number {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 0 0 10px currentColor;
}

/* 统计标签样式 */
.stat-label {
  font-size: 14px;
  color: #aaa;
}

/* 图表行样式 */
.chart-row {
  margin-bottom: 20px;
}

/* 图表卡片通用样式 */
.chart-card {
  background: rgba(30, 30, 46, 0.8);
  border: 1px solid rgba(79, 172, 254, 0.3);
  border-radius: 4px;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 20px rgba(79, 172, 254, 0.2);
  transition: all 0.3s ease;
}

/* 图表卡片悬停效果 */
.chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 30px rgba(79, 172, 254, 0.4);
  border-color: rgba(79, 172, 254, 0.6);
}

/* 图表卡片头部样式 */
.chart-card ::v-deep .el-card__header {
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 15px 20px;
}

/* 图表标题样式 */
.chart-header {
  color: #00f2fe;
  font-size: 18px;
  font-weight: bold;
}

/* 图表容器通用样式 */
.chart-container {
  width: 100%;
  height: 250px;  /* 小型分析卡250px */
}

/* 地图卡片特殊样式 */
.map-card .chart-container {
  height: 400px;  /* 地理分布卡400px */
}

/* 表格卡片特殊样式 */
.table-card .chart-container {
  height: 200px;  /* 表格卡200px */
}

.dark-table ::v-deep .el-table {
  background: transparent;
  color: #e0e0e0;
}

.dark-table ::v-deep .el-table__header th {
  background: rgba(0, 0, 0, 0.3);
  color: #00f2fe;
}

.dark-table ::v-deep .el-table__row {
  background: rgba(255, 255, 255, 0.02);
}

.dark-table ::v-deep .el-table__row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  color: #00f2fe;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(0, 242, 254, 0.3);
  border-top: 3px solid #00f2fe;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* ECharts暗色主题 */
::v-deep .echarts {
  color: #e0e0e0;
}

::v-deep .echarts text {
  fill: #e0e0e0;
}
</style>