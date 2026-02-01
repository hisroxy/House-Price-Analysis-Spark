"""
DWD.py - 数据仓库DWD层处理脚本
用于对ODS层数据进行清洗、转换和去重，生成高质量的明细层数据
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when, lower, regexp_replace, coalesce
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType

def create_dwd_table(spark: SparkSession) -> None:
    """
    创建DWD层表 dwd_house_data，对ODS层数据进行清洗和转换
    
    清洗规则：
    1. 去除字段前后空格
    2. 处理缺失值（用'未知'或0填充）
    3. 标准化价格字段（去除货币符号，转换为数值）
    4. 标准化面积字段（提取数字部分）
    5. 去重处理（基于关键字段组合）
    6. 添加数据质量标志字段
    """
    print("开始DWD层数据清洗处理...")
    
    # 读取ODS层数据
    ods_df = spark.table("ods_house_data")
    
    # 数据清洗和转换
    dwd_df = ods_df \
        .select(
            # 基础信息清洗
            trim(col("city")).alias("city"),
            trim(col("method")).alias("method"),
            trim(col("building_name")).alias("building_name"),
            trim(col("room_type")).alias("room_type"),
            trim(col("city_district")).alias("city_district"),
            trim(col("district_area")).alias("district_area"),
            
            # 面积字段清洗：提取数字部分，单位统一为平方米
            regexp_replace(trim(col("area")), r'[^\d\.]', '').cast(DoubleType()).alias("area_sqm"),
            
            # 朝向标准化
            trim(col("orientation")).alias("orientation"),
            
            # 标签清洗：去除多余空格，标准化格式
            trim(col("tags")).alias("tags"),
            
            # 价格字段清洗：去除货币符号和单位
            regexp_replace(trim(col("price")), r'[^\d\.]', '').cast(DoubleType()).alias("price"),
            
            # 楼层类型清洗
            trim(col("floor_type")).alias("floor_type"),
            
            # 楼层数清洗：提取数字部分
            regexp_replace(trim(col("floor_number")), r'[^\d]', '').cast(IntegerType()).alias("floor_number"),
            
            # 封面图和详情链接
            trim(col("cover_image")).alias("cover_image"),
            trim(col("detail_link")).alias("detail_link"),
            
            # 添加数据质量标志
            when(col("price").isNull() | (col("price") == 0), False)
             .when(col("area_sqm").isNull() | (col("area_sqm") == 0), False)
             .otherwise(True).alias("is_valid_data")
        ) \
        .filter(col("is_valid_data") == True) \
        .dropDuplicates(["building_name", "room_type", "city_district", "area_sqm", "price"]) \
        .fillna({
            "city": "未知",
            "method": "未知",
            "building_name": "未知",
            "room_type": "未知",
            "city_district": "未知",
            "district_area": "未知",
            "orientation": "未知",
            "tags": "未知",
            "floor_type": "未知",
            "cover_image": "无",
            "detail_link": "无"
        })
    
    # 显示清洗后的数据统计
    print(f"清洗前数据量: {ods_df.count()}")
    print(f"清洗后数据量: {dwd_df.count()}")
    print("数据清洗完成，开始创建DWD层表...")
    
    # 创建DWD层表
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS dwd_house_data (
        city STRING,
        method STRING,
        building_name STRING,
        room_type STRING,
        city_district STRING,
        district_area STRING,
        area_sqm DOUBLE,
        orientation STRING,
        tags STRING,
        price DOUBLE,
        floor_type STRING,
        floor_number INT,
        cover_image STRING,
        detail_link STRING,
        is_valid_data BOOLEAN
    )
    STORED AS ORC
    TBLPROPERTIES ("orc.compress"="SNAPPY")
    """
    
    # 执行创建表的SQL
    spark.sql(create_table_sql)
    
    # 将清洗后的数据写入DWD表
    dwd_df.write \
        .format("orc") \
        .mode("overwrite") \
        .saveAsTable("dwd_house_data")
    
    print("DWD层表 dwd_house_data 创建成功！")
    print("数据清洗和加载完成！")


if __name__ == "__main__":
    # 创建Spark会话
    spark = SparkSession.builder \
        .appName("CreateDWDETL") \
        .enableHiveSupport() \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.orc.impl", "native") \
        .getOrCreate()
    
    try:
        # 调用创建DWD表的函数
        create_dwd_table(spark)
    finally:
        # 关闭Spark会话
        spark.stop()