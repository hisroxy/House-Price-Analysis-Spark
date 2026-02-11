from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pyhive import hive
import json
import logging
from datetime import datetime
from user.models import UserFavoriteBehavior, UserDetailViewBehavior, UserCommentBehavior

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


def query_house_data(filters=None, page=1, page_size=20, sort_field='price', sort_order='asc'):
    """查询房屋数据"""
    conn = get_hive_connection()
    if not conn:
        return {'data': [], 'total': 0, 'page': page, 'page_size': page_size}
    
    try:
        cursor = conn.cursor()
        
        # 构建基础查询 - 移除is_valid_data限制，显示所有数据
        base_query = "SELECT city, method, building_name, room_type, city_district, district_area, area_sqm, orientation, tags, price, floor_type, floor_number, cover_image, detail_link, is_valid_data FROM dwd_house_data WHERE 1=1"
        count_query = "SELECT COUNT(*) FROM dwd_house_data WHERE 1=1"
        
        # 添加过滤条件
        where_conditions = []
        params = []
        
        if filters:
            # 城市过滤
            if filters.get('city'):
                where_conditions.append("city = %s")
                params.append(filters['city'])
            
            # 区域过滤
            if filters.get('city_district'):
                where_conditions.append("city_district = %s")
                params.append(filters['city_district'])
            
            # 户型过滤
            if filters.get('room_type'):
                where_conditions.append("room_type = %s")
                params.append(filters['room_type'])
            
            # 价格范围过滤
            if filters.get('min_price'):
                where_conditions.append("price >= %s")
                params.append(float(filters['min_price']))
            if filters.get('max_price'):
                where_conditions.append("price <= %s")
                params.append(float(filters['max_price']))
            
            # 面积范围过滤
            if filters.get('min_area'):
                where_conditions.append("area_sqm >= %s")
                params.append(float(filters['min_area']))
            if filters.get('max_area'):
                where_conditions.append("area_sqm <= %s")
                params.append(float(filters['max_area']))
            
            # 朝向过滤
            if filters.get('orientation'):
                where_conditions.append("orientation = %s")
                params.append(filters['orientation'])
            
            # 标签过滤
            if filters.get('tags'):
                where_conditions.append("tags LIKE %s")
                params.append(f"%{filters['tags']}%")
        
        # 构建WHERE子句
        if where_conditions:
            where_clause = " AND ".join(where_conditions)
            base_query += f" AND {where_clause}"
            count_query += f" AND {where_clause}"
        
        # 添加排序
        order_clause = f"ORDER BY {sort_field} {sort_order.upper()}"
        base_query += f" {order_clause}"
        
        # 添加分页
        offset = (page - 1) * page_size
        base_query += f" LIMIT {page_size} OFFSET {offset}"
        
        # 执行查询
        cursor.execute(base_query, params)
        results = cursor.fetchall()
        
        # 获取列名
        columns = [desc[0] for desc in cursor.description]
        
        # 转换为字典列表
        data = []
        for row in results:
            row_dict = {}
            for i, col_name in enumerate(columns):
                row_dict[col_name] = row[i]
            data.append(row_dict)
        
        # 获取总记录数
        cursor.execute(count_query, params)
        total_result = cursor.fetchone()
        total = total_result[0] if total_result else 0
        
        cursor.close()
        
        return {
            'data': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }
        
    except Exception as e:
        logger.error(f"查询房屋数据失败: {e}")
        return {'data': [], 'total': 0, 'page': page, 'page_size': page_size}
    finally:
        if conn:
            conn.close()


@csrf_exempt
def house_list(request):
    """获取房屋列表API"""
    if request.method == 'GET':
        try:
            # 获取查询参数
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 20))
            sort_field = request.GET.get('sort_field', 'price')
            sort_order = request.GET.get('sort_order', 'asc')
            
            # 获取过滤参数
            filters = {}
            if request.GET.get('city'):
                filters['city'] = request.GET.get('city')
            if request.GET.get('city_district'):
                filters['city_district'] = request.GET.get('city_district')
            if request.GET.get('room_type'):
                filters['room_type'] = request.GET.get('room_type')
            if request.GET.get('min_price'):
                filters['min_price'] = request.GET.get('min_price')
            if request.GET.get('max_price'):
                filters['max_price'] = request.GET.get('max_price')
            if request.GET.get('min_area'):
                filters['min_area'] = request.GET.get('min_area')
            if request.GET.get('max_area'):
                filters['max_area'] = request.GET.get('max_area')
            if request.GET.get('orientation'):
                filters['orientation'] = request.GET.get('orientation')
            if request.GET.get('tags'):
                filters['tags'] = request.GET.get('tags')
            
            # 查询数据
            result = query_house_data(filters, page, page_size, sort_field, sort_order)
            
            # 如果用户已登录，检查收藏状态
            if request.user.is_authenticated:
                favorite_house_ids = list(UserFavoriteBehavior.objects.filter(
                    user=request.user, is_active=True
                ).values_list('house_id', flat=True))
                
                # 为每个房屋添加收藏状态
                for house in result['data']:
                    house_id = f"{house['city']}_{house['building_name']}_{house['room_type']}"
                    house['is_favorite'] = house_id in favorite_house_ids
                    house['house_id'] = house_id
            else:
                for house in result['data']:
                    house['is_favorite'] = False
                    house_id = f"{house['city']}_{house['building_name']}_{house['room_type']}"
                    house['house_id'] = house_id
            
            return JsonResponse({
                'success': True,
                'data': result,
                'message': '数据获取成功'
            })
            
        except Exception as e:
            logger.error(f"获取房屋列表失败: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': '服务器内部错误'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def toggle_favorite(request):
    """切换收藏状态API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            house_id = data.get('house_id')
            
            if not house_id:
                return JsonResponse({
                    'success': False,
                    'message': '缺少房屋ID'
                }, status=400)
            
            # 检查是否已收藏
            favorite_record = UserFavoriteBehavior.objects.filter(
                user=request.user,
                house_id=house_id,
                is_active=True
            ).first()
            
            if favorite_record:
                # 取消收藏
                favorite_record.is_active = False
                favorite_record.save()
                is_favorite = False
                message = '取消收藏成功'
            else:
                # 添加收藏
                UserFavoriteBehavior.objects.create(
                    user=request.user,
                    house_id=house_id
                )
                is_favorite = True
                message = '收藏成功'
            
            return JsonResponse({
                'success': True,
                'data': {'is_favorite': is_favorite},
                'message': message
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            logger.error(f"切换收藏状态失败: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': '服务器内部错误'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def house_detail(request, house_id):
    """获取房屋详情API"""
    if request.method == 'GET':
        try:
            conn = get_hive_connection()
            if not conn:
                return JsonResponse({
                    'success': False,
                    'message': '数据库连接失败'
                }, status=500)
            
            try:
                cursor = conn.cursor()
                # 根据house_id查询详细信息
                query = """
                SELECT city, method, building_name, room_type, city_district, 
                       district_area, area_sqm, orientation, tags, price, 
                       floor_type, floor_number, cover_image, detail_link, is_valid_data
                FROM dwd_house_data 
                WHERE CONCAT(city, '_', building_name, '_', room_type) = %s 
                AND is_valid_data = TRUE
                LIMIT 1
                """
                
                cursor.execute(query, [house_id])
                result = cursor.fetchone()
                
                if not result:
                    return JsonResponse({
                        'success': False,
                        'message': '房屋信息不存在'
                    }, status=404)
                
                # 获取列名
                columns = [desc[0] for desc in cursor.description]
                
                # 转换为字典
                house_data = {}
                for i, col_name in enumerate(columns):
                    house_data[col_name] = result[i]
                
                # 添加收藏状态
                is_favorite = UserFavoriteBehavior.objects.filter(
                    user=request.user,
                    house_id=house_id,
                    is_active=True
                ).exists()
                house_data['is_favorite'] = is_favorite
                house_data['house_id'] = house_id
                
                # 记录查看详情行为
                UserDetailViewBehavior.objects.create(
                    user=request.user,
                    house_id=house_id
                )
                
                cursor.close()
                
                return JsonResponse({
                    'success': True,
                    'data': house_data,
                    'message': '数据获取成功'
                })
                
            finally:
                conn.close()
                
        except Exception as e:
            logger.error(f"获取房屋详情失败: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': '服务器内部错误'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def house_comments(request, house_id):
    """获取房屋评论API"""
    if request.method == 'GET':
        try:
            # 获取该房屋的所有评论
            comments = UserCommentBehavior.objects.filter(house_id=house_id).select_related('user')
            
            comment_data = []
            for comment in comments:
                comment_data.append({
                    'id': comment.id,
                    'user': {
                        'username': comment.user.username,
                        'nickname': getattr(comment.user.profile, 'nickname', comment.user.username) if hasattr(comment.user, 'profile') else comment.user.username
                    },
                    'comment': comment.comment,
                    'rating': comment.rating,
                    'commented_at': comment.commented_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return JsonResponse({
                'success': True,
                'data': comment_data,
                'message': '评论获取成功'
            })
            
        except Exception as e:
            logger.error(f"获取房屋评论失败: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': '服务器内部错误'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def add_comment(request, house_id):
    """添加评论API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_text = data.get('comment', '').strip()
            rating = data.get('rating')
            
            if not comment_text:
                return JsonResponse({
                    'success': False,
                    'message': '评论内容不能为空'
                }, status=400)
            
            # 验证评分范围
            if rating is not None:
                try:
                    rating = int(rating)
                    if rating < 1 or rating > 5:
                        return JsonResponse({
                            'success': False,
                            'message': '评分必须在1-5之间'
                        }, status=400)
                except (ValueError, TypeError):
                    rating = None
            
            # 添加评论
            comment = UserCommentBehavior.objects.create(
                user=request.user,
                house_id=house_id,
                comment=comment_text,
                rating=rating
            )
            
            return JsonResponse({
                'success': True,
                'data': {
                    'id': comment.id,
                    'user': {
                        'username': request.user.username,
                        'nickname': getattr(request.user.profile, 'nickname', request.user.username) if hasattr(request.user, 'profile') else request.user.username
                    },
                    'comment': comment_text,
                    'rating': rating,
                    'commented_at': comment.commented_at.strftime('%Y-%m-%d %H:%M:%S')
                },
                'message': '评论发表成功'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            logger.error(f"添加评论失败: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': '服务器内部错误'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
