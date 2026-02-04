"""
sparkDashboardBig.py - 房价分析大屏数据处理脚本
用于生成Dashboard大屏所需的各类数据分析和可视化数据
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max, min, round as spark_round
import json
import os
from datetime import datetime

def analyze_overview_data(spark: SparkSession) -> None:
    """分析总体数据概览并保存到Hive表"""
    try:
        df = spark.table("dwd_house_data")
        total_count = df.count()
        avg_price = df.agg(avg("price")).collect()[0][0]
        max_price = df.agg(max("price")).collect()[0][0]
        min_price = df.agg(min("price")).collect()[0][0]
        
        # 创建概览数据DataFrame
        from pyspark.sql.types import StructType, StructField, StringType, DoubleType
        schema = StructType([
            StructField("metric_name", StringType(), True),
            StructField("metric_value", DoubleType(), True)
        ])
        
        overview_data = [
            ("total_houses", float(total_count)),
            ("avg_price", float(avg_price) if avg_price else 0.0),
            ("max_price", float(max_price) if max_price else 0.0),
            ("min_price", float(min_price) if min_price else 0.0)
        ]
        
        overview_df = spark.createDataFrame(overview_data, schema)
        overview_df.write.mode("overwrite").saveAsTable("sparkDashboardBig_overview")
        print("概览数据已保存到Hive表: sparkDashboardBig_overview")
        
    except Exception as e:
        print(f"概览数据分析失败: {e}")

def analyze_price_trend(spark: SparkSession) -> None:
    """分析价格趋势（按城市分组）"""
    try:
        df = spark.table("dwd_house_data")
        trend_data = df.groupBy("city") \
            .agg(
                avg("price").alias("avg_price"),
                count("*").alias("house_count"),
                max("price").alias("max_price")
            ) \
            .orderBy(col("avg_price").desc()) \
            .limit(10) \
            .collect()
        
        # 保存到Hive表
        trend_df = spark.createDataFrame([
            (row.city, round(float(row.avg_price), 2), int(row.house_count), float(row.max_price))
            for row in trend_data
        ], ["city", "avg_price", "house_count", "max_price"])
        
        trend_df.write.mode("overwrite").saveAsTable("sparkDashboardBig_price_trend")
    except Exception as e:
        print(f"价格趋势分析失败: {e}")

def analyze_area_distribution(spark: SparkSession) -> None:
    """分析区域房源分布"""
    try:
        df = spark.table("dwd_house_data")
        area_data = df.groupBy("city_district") \
            .agg(count("*").alias("count")) \
            .orderBy(col("count").desc()) \
            .limit(15) \
            .collect()
        
        # 保存到Hive表
        area_df = spark.createDataFrame([
            (row.city_district, int(row['count']))
            for row in area_data
        ], ["city_district", "count"])
        
        area_df.write.mode("overwrite").saveAsTable("sparkDashboardBig_area_distribution")
    except Exception as e:
        print(f"区域分布分析失败: {e}")

def analyze_room_type_stats(spark: SparkSession) -> None:
    """分析户型统计"""
    try:
        df = spark.table("dwd_house_data")
        room_data = df.groupBy("room_type") \
            .agg(
                count("*").alias("count"),
                avg("price").alias("avg_price")
            ) \
            .orderBy(col("count").desc()) \
            .limit(10) \
            .collect()
        
        # 保存到Hive表
        room_df = spark.createDataFrame([
            (row.room_type, int(row['count']), round(float(row['avg_price']), 2) if row['avg_price'] else 0)
            for row in room_data
        ], ["room_type", "count", "avg_price"])
        
        room_df.write.mode("overwrite").saveAsTable("sparkDashboardBig_room_type_stats")
    except Exception as e:
        print(f"户型统计分析失败: {e}")

def analyze_orientation_stats(spark: SparkSession) -> None:
    """分析朝向统计"""
    try:
        df = spark.table("dwd_house_data")
        orientation_data = df.groupBy("orientation") \
            .agg(count("*").alias("count")) \
            .orderBy(col("count").desc()) \
            .limit(8) \
            .collect()
        
        # 保存到Hive表
        orientation_df = spark.createDataFrame([
            (row.orientation, int(row['count']))
            for row in orientation_data
        ], ["orientation", "count"])
        
        orientation_df.write.mode("overwrite").saveAsTable("sparkDashboardBig_orientation_stats")
    except Exception as e:
        print(f"朝向统计分析失败: {e}")

def analyze_price_range_distribution(spark: SparkSession) -> None:
    """分析价格区间分布"""
    try:
        df = spark.table("dwd_house_data")
        price_ranges = [
            (0, 3000, "0-3000元"),
            (3000, 5000, "3000-5000元"),
            (5000, 8000, "5000-8000元"),
            (8000, 12000, "8000-12000元"),
            (12000, 20000, "12000-20000元"),
            (20000, float('inf'), "20000元以上")
        ]
        
        # 计算各价格区间的数量并保存到Hive表
        price_range_data = []
        for min_price, max_price, label in price_ranges:
            if max_price == float('inf'):
                count_result = df.filter(col("price") >= min_price).count()
            else:
                count_result = df.filter((col("price") >= min_price) & (col("price") < max_price)).count()
            price_range_data.append((label, int(count_result)))
        
        # 保存到Hive表
        price_range_df = spark.createDataFrame(price_range_data, ["price_range", "count"])
        price_range_df.write.mode("overwrite").saveAsTable("sparkdashboardbig_price_range_distribution")
    except Exception as e:
        print(f"价格区间分析失败: {e}")

def analyze_tags_wordcloud(spark: SparkSession) -> None:
    """分析标签词云数据"""
    try:
        df = spark.table("dwd_house_data")
        tags_data = df.select("tags").collect()
        
        tag_count = {}
        for row in tags_data:
            if row.tags and row.tags != "未知":
                tags = row.tags.split("、")
                for tag in tags:
                    tag = tag.strip()
                    if tag:
                        tag_count[tag] = tag_count.get(tag, 0) + 1
        
        sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:30]
        
        # 保存到Hive表
        tags_df = spark.createDataFrame([
            (tag, count)
            for tag, count in sorted_tags
        ], ["tag", "count"])
        
        tags_df.write.mode("overwrite").saveAsTable("sparkDashboardBig_tags_wordcloud")
    except Exception as e:
        print(f"标签词云分析失败: {e}")

def generate_dashboard_data(spark: SparkSession) -> None:
    """生成完整的dashboard数据并保存到Hive表"""
    print("开始生成大屏数据...")
    
    # 执行各项分析并将结果保存到对应的Hive表
    analyze_overview_data(spark)
    analyze_price_trend(spark)
    analyze_area_distribution(spark)
    analyze_room_type_stats(spark)
    analyze_orientation_stats(spark)
    analyze_price_range_distribution(spark)
    analyze_tags_wordcloud(spark)
    
    print("大屏数据已全部保存到Hive表!")

if __name__ == "__main__":
    # 创建Spark会话
    spark = SparkSession.builder \
        .appName("DashboardDataGeneration") \
        .enableHiveSupport() \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()
    
    try:
        # 生成dashboard数据
        generate_dashboard_data(spark)
    finally:
        spark.stop()