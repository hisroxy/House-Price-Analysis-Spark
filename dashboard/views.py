from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyhive import hive
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 导入Hive配置
from backend.db_config import HIVE_CONFIG

def get_hive_connection(retry_count=3):
    """获取Hive连接，带重试机制"""
    try:
        conn = hive.Connection(
            host=HIVE_CONFIG['host'],
            port=HIVE_CONFIG['port'],
            username=HIVE_CONFIG['username'],
            password=HIVE_CONFIG['password'],
            database=HIVE_CONFIG['database'],
            auth=HIVE_CONFIG['auth']
        )
        return conn
    except Exception as e:
        logger.error(f"Hive连接失败: {e}")
        return None


def query_hive_table(table_name):
    """查询Hive表数据"""
    conn = get_hive_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # 转换为字典列表
        data = []
        for row in results:
            row_dict = {}
            for i, col_name in enumerate(columns):
                row_dict[col_name] = row[i]
            data.append(row_dict)
        
        cursor.close()
        return data
    except Exception as e:
        logger.error(f"查询表 {table_name} 失败: {e}")
        return []
    finally:
        if conn:
            conn.close()

def dashboard_view(request):
    """返回dashboard页面"""
    return render(request, 'dashboard.html')

@csrf_exempt
def dashboard_data(request):
    """获取dashboard大屏数据API"""
    if request.method == 'GET':
        try:
            # 从Hive表读取数据（使用正确大小写表名）
            overview_data = query_hive_table("sparkDashboardBig_overview")
            price_trend_data = query_hive_table("sparkDashboardBig_price_trend")
            area_dist_data = query_hive_table("sparkDashboardBig_area_distribution")
            room_type_data = query_hive_table("sparkDashboardBig_room_type_stats")
            orientation_data = query_hive_table("sparkDashboardBig_orientation_stats")
            price_range_data = query_hive_table("sparkdashboardbig_price_range_distribution")
            tags_data = query_hive_table("sparkDashboardBig_tags_wordcloud")
            
            # 格式化数据
            formatted_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "overview": {},
                "price_trend": [],
                "area_distribution": [],
                "room_type_stats": [],
                "orientation_stats": [],
                "price_range_distribution": [],
                "tags_wordcloud": []
            }
            
            # 处理概览数据
            for row in overview_data:
                formatted_data["overview"][row["metric_name"]] = row["metric_value"]
            
            # 处理价格趋势数据
            for row in price_trend_data:
                formatted_data["price_trend"].append({
                    "city": row["city"],
                    "avg_price": float(row["avg_price"]),
                    "house_count": int(row["house_count"]),
                    "max_price": float(row["max_price"])
                })
            
            # 处理区域分布数据
            for row in area_dist_data:
                formatted_data["area_distribution"].append({
                    "name": row["city_district"],
                    "value": int(row["count"])
                })
            
            # 处理户型统计数据
            for row in room_type_data:
                formatted_data["room_type_stats"].append({
                    "room_type": row["room_type"],
                    "count": int(row["count"]),
                    "avg_price": float(row["avg_price"])
                })
            
            # 处理朝向统计数据
            for row in orientation_data:
                formatted_data["orientation_stats"].append({
                    "name": row["orientation"],
                    "value": int(row["count"])
                })
            
            # 处理价格区间数据
            for row in price_range_data:
                formatted_data["price_range_distribution"].append({
                    "range": row["price_range"],
                    "count": int(row["count"])
                })
            
            # 处理标签词云数据
            for row in tags_data:
                formatted_data["tags_wordcloud"].append({
                    "name": row["tag"],
                    "value": int(row["count"])
                })
            
            return JsonResponse({
                'success': True,
                'data': formatted_data,
                'message': '数据获取成功'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': '服务器内部错误'
            }, status=500)

@csrf_exempt
def dashboard_summary(request):
    """获取dashboard大屏摘要数据API（用于自动翻滚榜单）"""
    if request.method == 'GET':
        try:
            # 从Hive表读取数据（使用正确大小写表名）
            overview_data = query_hive_table("sparkDashboardBig_overview")
            price_trend_data = query_hive_table("sparkDashboardBig_price_trend")
            area_dist_data = query_hive_table("sparkDashboardBig_area_distribution")
            room_type_data = query_hive_table("sparkDashboardBig_room_type_stats")
            
            # 格式化摘要数据（用于自动翻滚榜单）
            summary_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_houses": 0,
                "avg_price": 0,
                "top_cities": [],
                "top_areas": [],
                "top_room_types": []
            }
            
            # 处理概览数据
            for row in overview_data:
                if row["metric_name"] == "total_houses":
                    summary_data["total_houses"] = int(row["metric_value"])
                elif row["metric_name"] == "avg_price":
                    summary_data["avg_price"] = float(row["metric_value"])
            
            # 处理价格趋势（前3个城市）
            for i, row in enumerate(price_trend_data[:3]):
                summary_data["top_cities"].append({
                    "rank": i+1,
                    "city": row["city"],
                    "avg_price": float(row["avg_price"]),
                    "house_count": int(row["house_count"])
                })
            
            # 处理区域分布（前3个区域）
            for i, row in enumerate(area_dist_data[:3]):
                summary_data["top_areas"].append({
                    "rank": i+1,
                    "area": row["city_district"],
                    "count": int(row["count"])
                })
            
            # 处理户型统计（前3种户型）
            for i, row in enumerate(room_type_data[:3]):
                summary_data["top_room_types"].append({
                    "rank": i+1,
                    "room_type": row["room_type"],
                    "count": int(row["count"]),
                    "avg_price": float(row["avg_price"])
                })
            
            return JsonResponse({
                'success': True,
                'data': summary_data,
                'message': '摘要数据获取成功'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': '服务器内部错误'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)