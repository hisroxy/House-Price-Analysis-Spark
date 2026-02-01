from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

def create_external_table(spark: SparkSession) -> None:
    """
    创建ODS层外部Hive表，链接HDFS上的CSV文件
    
    表结构基于爬虫获取的房屋数据字段，使用英文命名
    数据源路径: /houseData/house.csv (由upload_hdfs.py上传)
    """
    # 定义表结构（根据spiderMain.py中爬取的字段）
    schema = StructType([
        StructField("city", StringType(), True),           # 城市
        StructField("method", StringType(), True),         # 方式(出租/出售)
        StructField("building_name", StringType(), True),  # 楼盘名称
        StructField("room_type", StringType(), True),      # 户型
        StructField("city_district", StringType(), True),  # 城市地区
        StructField("district_area", StringType(), True),  # 区内地段
        StructField("area", StringType(), True),           # 面积
        StructField("orientation", StringType(), True),    # 朝向
        StructField("tags", StringType(), True),           # 标签
        StructField("price", StringType(), True),          # 价格
        StructField("floor_type", StringType(), True),     # 楼层类型
        StructField("floor_number", StringType(), True),   # 楼层数
        StructField("cover_image", StringType(), True),    # 封面图
        StructField("detail_link", StringType(), True)     # 详情链接
    ])
    
    # 读取HDFS上的CSV文件
    df = spark.read \
        .option("header", "true") \
        .option("delimiter", ",") \
        .schema(schema) \
        .csv("/houseData/house.csv")
    
    # 创建外部表
    # 注意：这里使用Hive SQL创建外部表，确保Hive Metastore已配置
    create_table_sql = """
    CREATE EXTERNAL TABLE IF NOT EXISTS ods_house_data (
        city STRING,
        method STRING,
        building_name STRING,
        room_type STRING,
        city_district STRING,
        district_area STRING,
        area STRING,
        orientation STRING,
        tags STRING,
        price STRING,
        floor_type STRING,
        floor_number STRING,
        cover_image STRING,
        detail_link STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION '/houseData'
    TBLPROPERTIES ("skip.header.line.count"="1")
    """
    
    # 执行创建表的SQL
    spark.sql(create_table_sql)
    
    print("ODS层外部表 ods_house_data 创建成功！")
    print("表结构已定义，数据源指向 HDFS 路径: /houseData/house.csv")


if __name__ == "__main__":
    # 创建Spark会话
    spark = SparkSession.builder \
        .appName("CreateODSTable") \
        .enableHiveSupport() \
        .getOrCreate()
    
    # 调用创建外部表的函数
    create_external_table(spark)
    
    # 关闭Spark会话
    spark.stop()