<template>
  <div class="houses">
    <h1>房价列表</h1>
    <el-table :data="houses" style="width: 100%">
      <el-table-column prop="id" label="ID" width="180"></el-table-column>
      <el-table-column prop="title" label="标题" width="180"></el-table-column>
      <el-table-column prop="price" label="价格"></el-table-column>
      <el-table-column prop="location" label="位置"></el-table-column>
      <el-table-column prop="area" label="面积"></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'Houses',
  data() {
    return {
      houses: []
    }
  },
  mounted() {
    this.loadHouses()
  },
  methods: {
    loadHouses() {
      // 模拟加载房价数据
      this.houses = [
        { id: 1, title: '温馨两居室', price: 3500000, location: '北京市朝阳区', area: 85 },
        { id: 2, title: '豪华三居室', price: 6800000, location: '上海市浦东新区', area: 120 }
      ]
    }
  }
}
</script>