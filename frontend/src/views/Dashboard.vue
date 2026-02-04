<template>
  <div class="dashboard dark-theme">
    <!-- 顶部概览卡片 -->
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
    
    <!-- 第一行：地图和价格趋势 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">广东省房源地理分布</div>
          <div ref="mapChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">城市均价排行</div>
          <div ref="priceTrendChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 第二行：区域分布和户型统计 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">区域房源分布</div>
          <div ref="areaChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">户型统计分析</div>
          <div ref="roomTypeChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 第三行：朝向分布和价格区间 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">房源朝向分布</div>
          <div ref="orientationChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">价格区间分布</div>
          <div ref="priceRangeChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 第四行：词云图和数据表格 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">房源标签词云</div>
          <div ref="wordCloudChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header" class="chart-header">详细数据表格</div>
          <el-table :data="tableData" height="350" stripe class="dark-table">
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
    
    <!-- 加载提示 -->
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
      loading: false,
      dashboardData: {},
      charts: {}
    }
  },
  computed: {
    overviewStats() {
      const data = this.dashboardData.overview || {}
      return [
        { label: '房源总数', value: (data.total_houses || 0).toLocaleString(), color: '#409EFF' },
        { label: '平均价格', value: `¥${(data.avg_price || 0).toLocaleString()}`, color: '#67C23A' },
        { label: '最高价格', value: `¥${(data.max_price || 0).toLocaleString()}`, color: '#E6A23C' },
        { label: '最低价格', value: `¥${(data.min_price || 0).toLocaleString()}`, color: '#F56C6C' }
      ]
    },
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
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        // 使用mock数据
        this.dashboardData = this.generateMockData()
      } finally {
        this.loading = false
      }
    },
    initCharts() {
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
    },
    generateMockData() {
      return {
        overview: { total_houses: 15678, avg_price: 7800.50, max_price: 25000, min_price: 1200 },
        price_trend: [
          { city: '深圳', avg_price: 8500, house_count: 4200, max_price: 25000 },
          { city: '广州', avg_price: 6800, house_count: 3800, max_price: 20000 },
          { city: '东莞', avg_price: 4200, house_count: 2900, max_price: 15000 }
        ],
        area_distribution: [
          { name: '南山区', value: 1850 }, { name: '福田区', value: 1620 },
          { name: '宝安区', value: 1430 }, { name: '龙岗区', value: 1280 }
        ],
        room_type_stats: [
          { room_type: '3室2厅', count: 5200, avg_price: 7200 },
          { room_type: '2室1厅', count: 4800, avg_price: 5800 },
          { room_type: '1室1厅', count: 2100, avg_price: 3200 }
        ],
        orientation_stats: [
          { name: '南', value: 4200 }, { name: '南北', value: 3800 },
          { name: '东', value: 2100 }, { name: '西', value: 1800 }
        ],
        price_range_distribution: [
          { range: '0-3000元', count: 1200 }, { range: '3000-5000元', count: 3800 },
          { range: '5000-8000元', count: 5200 }, { range: '8000-12000元', count: 3100 }
        ],
        tags_wordcloud: [
          { name: '近地铁', value: 6800 }, { name: '精装', value: 5200 },
          { name: '随时看房', value: 4800 }, { name: '新上', value: 3900 }
        ]
      }
    }
  }
}
</script>

<style scoped>
.dark-theme {
  background: #0a1929;
  color: #e0e0e0;
  min-height: 100vh;
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.stat-card ::v-deep .el-card__body {
  padding: 20px;
}

.stat-content {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 0 0 10px currentColor;
}

.stat-label {
  font-size: 14px;
  color: #aaa;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.chart-card ::v-deep .el-card__header {
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 15px 20px;
}

.chart-header {
  color: #00f2fe;
  font-size: 18px;
  font-weight: bold;
}

.chart-container {
  width: 100%;
  height: 350px;
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