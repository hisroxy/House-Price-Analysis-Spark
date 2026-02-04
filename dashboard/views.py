from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyhive import hive
import json
from datetime import datetime

def get_hive_connection():
    """获取Hive连接"""
    try:
        conn = hive.Connection(host='localhost', port=10000, username='hive')
        return conn
    except Exception as e:
        print(f"Hive连接失败: {e}")
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
        
        return data
    except Exception as e:
        print(f"查询表 {table_name} 失败: {e}")
        return []
    finally:
        if conn:
            conn.close()

@csrf_exempt
def dashboard_data(request):
    """获取dashboard大屏数据API"""
    if request.method == 'GET':
        try:
            # 从Hive表读取数据
            overview_data = query_hive_table("sparkDashboardBig_overview")
            price_trend_data = query_hive_table("sparkDashboardBig_price_trend")
            area_dist_data = query_hive_table("sparkDashboardBig_area_distribution")
            room_type_data = query_hive_table("sparkDashboardBig_room_type_stats")
            orientation_data = query_hive_table("sparkDashboardBig_orientation_stats")
            price_range_data = query_hive_table("sparkDashboardBig_price_range_distribution")
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
                    "count": int(row["house_count"])
                })
            
            # 处理标签词云数据
            for row in tags_data:
                formatted_data["tags_wordcloud"].append({
                    "name": row["tag_name"],
                    "value": int(row["tag_count"])
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
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)