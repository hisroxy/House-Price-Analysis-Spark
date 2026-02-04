# House-Price-Analysis-Spark

基于Spark的大数据房价分析与智能推荐系统

## 🏠 项目简介

这是一个集数据采集、大数据处理、智能分析于一体的房价分析平台。系统通过爬取链家网房源数据，利用Spark进行大数据处理，结合用户行为数据实现个性化房源推荐。

## 🏗️ 技术架构

### 前端技术栈
- **Vue 2.6.14** - 渐进式JavaScript框架
- **Element UI 2.15.6** - 组件库
- **ECharts 5.4.3** - 数据可视化
- **Vuex 3.6.2** - 状态管理
- **Vue Router 3.5.1** - 路由管理

### 后端技术栈
- **Django 3.2** - Python Web框架
- **Django REST Framework** - RESTful API开发
- **MySQL 8.0** - 关系型数据库
- **PyMySQL** - MySQL驱动

### 大数据技术栈
- **Apache Spark 3.5.8** - 大数据处理引擎
- **Apache Hive** - 数据仓库工具
- **HDFS** - 分布式文件系统
- **PyHive 0.7.0** - Python Hive客户端

### 数据采集
- **BeautifulSoup4** - HTML解析
- **DrissionPage** - 浏览器自动化
- **Requests** - HTTP请求库

## 📁 项目结构

```
House-Price-Analysis-Spark/
├── backend/                 # Django后端
│   ├── settings.py         # 配置文件
│   ├── urls.py            # URL路由
│   └── wsgi.py            # WSGI部署
├── frontend/               # Vue前端
│   ├── src/
│   │   ├── main.js        # 注册Element UI,挂载Router、Store，渲染App.vue。
│   │   ├── App.vue        # 布局根组件，引用HeaderBar并渲染路由出口。
│   │   ├── components/
│   │   │   ├── HeaderBar.vue   #顶部导航，展示产品名称与菜单占位。        
│   │   ├── router/        # 路由配置
│   │   │   ├── index.js   #使用history模式,目前/指向Dashboard    
│   │   ├── store/         # 状态管理
│   │   │   ├── index.js   #Vuex 状态管理, 内 userStats、recommendationPreview, fetchDashboardbata 填静态数据。    
│   │   └── views/         # 页面组件
│   │       ├── Dashboard.vue   # 使用Element UI的el-row/el-card渲染指标卡与推荐列表，
│   ├── package.json       # 前端依赖，Vue CLI 4 项目描述, 依赖 vue@2.6、vue-router、vuex、element-ui、echarts,脚本含serve/build/lint。
│   └──vue.config.js        #可配置方向代理（目前保持默认配置）
├── user/                   # 用户管理应用
│   ├── models.py          # 用户数据模型
│   ├── views.py           # 用户视图
│   └── urls.py            # 用户路由
├── houses/                 # 房价数据应用（目前为占位app、后续用于对接房价数据）
│   ├── views.py           # 房价视图
│   └── urls.py            # 房价路由
├── recommend/              # 推荐系统应用（目前为占位app、后续用于对接房屋推荐）
│   ├── views.py           # 推荐视图
│   └── urls.py            # 推荐路由
├── spider/                 # 数据爬虫
│   ├── spiderMain.py      # 链家网爬虫
│   ├── city.txt           # 城市配置
│   └── house.csv          # 爬取数据
├── spark/                  # Spark处理
│   ├── upload_hdfs.py     # 数据上传
│   ├── ODS.py            # ODS层处理
│   └── DWD.py            # DWD层清洗
├── manage.py              # Django管理命令
├── requirements.txt       # Python依赖
└── init_project.py        # 项目初始化
```

## 🔧 环境配置

### 前置条件
- Python 3.8+
- Node.js 14+
- MySQL 8.0
- Java 8+ (Spark运行环境)
- Hadoop集群 (可选)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd House-Price-Analysis-Spark
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **安装前端依赖**
```bash
cd frontend
npm install
```

4. **数据库配置**
```sql
CREATE DATABASE train_houses CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **初始化项目**
```bash
python init_project.py
```

## 🚀 运行项目

### 启动后端服务
```bash
python manage.py runserver 8000
```

### 启动前端服务
```bash
cd frontend
npm run dev
```

### 数据处理流程

1. **运行爬虫采集数据**
```bash
cd spider
python spiderMain.py
```

2. **上传数据到HDFS**
```bash
cd spark
python upload_hdfs.py
```

3. **执行Spark数据处理**
```bash
spark-submit ODS.py
spark-submit DWD.py
```

## 📊 核心功能

### 数据采集模块
- 支持多城市房源数据爬取
- 智能验证码识别处理
- 完整房源信息采集(14个维度)

### 数据处理模块
- **ODS层**: 原始数据接入与存储
- **DWD层**: 数据清洗与标准化
- **DWS层**: 数据汇总与聚合(待实现)
- **ADS层**: 应用数据服务(待实现)

### 用户管理模块
- 用户注册/登录
- 个人信息管理
- 用户行为追踪(点击、浏览、收藏、评论)

### 房价分析模块
- 房源数据展示
- 地理分布可视化
- 户型统计分析

### 智能推荐模块


## 🗄️ 数据库设计

### 用户相关表
- `UserProfile` - 用户基本信息
- `UserClickBehavior` - 用户点击行为
- `UserDetailViewBehavior` - 用户详情浏览行为
- `UserFavoriteBehavior` - 用户收藏行为
- `UserCommentBehavior` - 用户评论行为

### 房源数据表
- `ods_house_data` - 原始房源数据(Hive表)
- `dwd_house_data` - 清洗后房源数据(Hive表)

## 📈 数据字段说明

爬虫采集的房源数据包含以下字段：
- 城市、租赁方式、楼盘名称
- 户型、面积、朝向
- 城市、区内地段
- 价格、楼层信息、标签
- 封面图片、详情链接、品牌



## 🔧 配置说明

### 数据库配置 (backend/settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'train_houses',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### HDFS配置 (spark/upload_hdfs.py)
```python
HDFS_HOST = "http://node1:9870"
HDFS_TARGET_PATH = "/houseData/house2.csv"
HDFS_USER = "root"
```

### 爬虫配置 (spider/spiderMain.py)
```python
# 支持的城市列表
selected_city_code = 'sz'  # 深圳
# 可选: gz(广州), fs(佛山), dg(东莞)等
```

## 🛠️ 开发指南

### API接口规范
- 所有API接口均以`/api/`开头
- 使用JSON格式进行数据交换
- 遵循RESTful设计原则

### 前端开发
- 组件化开发模式
- 使用Vuex进行状态管理
- 响应式设计适配移动端

### 后端开发
- MVC架构模式
- 数据库迁移使用Django ORM
- API文档待完善

## 📝 待办事项

- [ ] 完善推荐算法核心逻辑
- [ ] 实现DWS和ADS数据层
- [ ] 添加数据监控和告警机制
- [ ] 优化前端用户体验
- [ ] 完善API文档
- [ ] 添加单元测试
- [ ] 部署生产环境配置

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请联系项目维护者。

---
*基于大数据技术的智能房价分析平台*