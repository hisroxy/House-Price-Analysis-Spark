<template>
  <div class="recommend">
    <h1>推荐房源</h1>
    <el-button @click="loadRecommendations">获取推荐</el-button>
    <el-table :data="recommendations" style="width: 100%" v-if="recommendations.length > 0">
      <el-table-column prop="id" label="ID" width="180"></el-table-column>
      <el-table-column prop="title" label="标题" width="180"></el-table-column>
      <el-table-column prop="price" label="价格"></el-table-column>
      <el-table-column prop="location" label="位置"></el-table-column>
      <el-table-column prop="score" label="推荐得分"></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'Recommend',
  data() {
    return {
      recommendations: []
    }
  },
  methods: {
    loadRecommendations() {
      // 模拟加载推荐数据
      this.recommendations = [
        { id: 'rec1', title: '个性化推荐房源1', price: 4200000, location: '北京市海淀区', score: 0.95 },
        { id: 'rec2', title: '个性化推荐房源2', price: 3800000, location: '上海市静安区', score: 0.92 }
      ]
    }
  }
}
</script>