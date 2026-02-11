from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import UserProfile, UserClickBehavior, UserDetailViewBehavior, UserFavoriteBehavior, UserCommentBehavior
import json
import re
from datetime import datetime

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """
    用户注册API
    """
    try:
        data = json.loads(request.body)
        
        # 验证必填字段
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return JsonResponse({
                'success': False,
                'message': '用户名、邮箱和密码不能为空'
            }, status=400)
        
        # 验证邮箱格式
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return JsonResponse({
                'success': False,
                'message': '邮箱格式不正确'
            }, status=400)
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': '用户名已存在'
            }, status=400)
        
        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': '邮箱已被注册'
            }, status=400)
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # 创建用户资料
        profile_data = {
            'nickname': data.get('nickname', username),
            'phone': data.get('phone', ''),
            'gender': data.get('gender', '未知'),
            'city': data.get('city', ''),
            'avatar': data.get('avatar', ''),
        }
        
        # 处理出生日期
        birth_date_str = data.get('birth_date', '')
        if birth_date_str:
            try:
                profile_data['birth_date'] = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        UserProfile.objects.create(user=user, **profile_data)
        
        return JsonResponse({
            'success': True,
            'message': '注册成功',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': '请求数据格式错误'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """
    用户登录API
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'message': '用户名和密码不能为空'
            }, status=400)
        
        # 认证用户
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # 获取用户资料
            try:
                profile = user.profile
                user_info = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'nickname': profile.nickname or user.username,
                    'phone': profile.phone or '',
                    'gender': profile.gender or '未知',
                    'city': profile.city or '',
                    'avatar': profile.avatar or '',
                    'birth_date': profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else ''
                }
            except UserProfile.DoesNotExist:
                # 如果没有用户资料，创建默认资料
                profile = UserProfile.objects.create(user=user)
                user_info = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'nickname': user.username,
                    'phone': '',
                    'gender': '未知',
                    'city': '',
                    'avatar': '',
                    'birth_date': ''
                }
            
            return JsonResponse({
                'success': True,
                'message': '登录成功',
                'data': user_info
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '用户名或密码错误'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': '请求数据格式错误'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["POST"])
def logout_user(request):
    """
    用户退出登录API
    """
    try:
        logout(request)
        return JsonResponse({
            'success': True,
            'message': '退出登录成功'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'退出登录失败: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_user_info(request):
    """
    获取当前用户信息API
    """
    try:
        user = request.user
        try:
            profile = user.profile
            user_info = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'nickname': profile.nickname or user.username,
                'phone': profile.phone or '',
                'gender': profile.gender or '未知',
                'city': profile.city or '',
                'avatar': profile.avatar or '',
                'birth_date': profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else ''
            }
        except UserProfile.DoesNotExist:
            user_info = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'nickname': user.username,
                'phone': '',
                'gender': '未知',
                'city': '',
                'avatar': '',
                'birth_date': ''
            }
        
        return JsonResponse({
            'success': True,
            'data': user_info
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'获取用户信息失败: {str(e)}'
        }, status=500)

@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def update_user_info(request):
    """
    更新用户信息API
    """
    try:
        data = json.loads(request.body)
        user = request.user
        
        # 更新User表字段
        if 'email' in data:
            user.email = data['email']
            user.save()
        
        # 更新UserProfile表字段
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        # 更新可选字段
        update_fields = []
        if 'phone' in data:
            profile.phone = data['phone']
            update_fields.append('phone')
        if 'gender' in data:
            profile.gender = data['gender']
            update_fields.append('gender')
        if 'nickname' in data:
            profile.nickname = data['nickname']
            update_fields.append('nickname')
        if 'city' in data:
            profile.city = data['city']
            update_fields.append('city')
        if 'avatar' in data:
            profile.avatar = data['avatar']
            update_fields.append('avatar')
        if 'birth_date' in data and data['birth_date']:
            try:
                profile.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
                update_fields.append('birth_date')
            except ValueError:
                pass
        
        if update_fields:
            profile.save(update_fields=update_fields)
        
        # 返回更新后的用户信息
        updated_user_info = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'nickname': profile.nickname or user.username,
            'phone': profile.phone or '',
            'gender': profile.gender or '未知',
            'city': profile.city or '',
            'avatar': profile.avatar or '',
            'birth_date': profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else ''
        }
        
        return JsonResponse({
            'success': True,
            'message': '用户信息更新成功',
            'data': updated_user_info
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': '请求数据格式错误'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'更新用户信息失败: {str(e)}'
        }, status=500)
