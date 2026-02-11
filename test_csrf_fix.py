#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试CSRF修复的脚本
验证前端axios配置和后端视图修改是否正确
"""

import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from user.views import update_user_info
from django.test import RequestFactory
from django.contrib.auth.models import User
from user.models import UserProfile
import json

def test_csrf_exempt_decorator():
    """测试update_user_info视图是否正确添加了csrf_exempt装饰器"""
    print("=== 测试CSRF装饰器修复 ===")
    
    # 检查视图函数的装饰器
    import inspect
    from django.views.decorators.csrf import csrf_exempt
    
    # 获取视图函数的源码
    source = inspect.getsource(update_user_info)
    print("视图函数源码:")
    print(source[:200] + "..." if len(source) > 200 else source)
    
    # 检查是否有csrf_exempt装饰器
    if hasattr(update_user_info, 'csrf_exempt'):
        print("✅ 视图已正确添加 @csrf_exempt 装饰器")
        return True
    else:
        print("❌ 视图缺少 @csrf_exempt 装饰器")
        return False

def test_frontend_config():
    """测试前端配置文件修改"""
    print("\n=== 测试前端配置修复 ===")
    
    frontend_config_path = "frontend/src/main.js"
    if os.path.exists(frontend_config_path):
        with open(frontend_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查关键配置项
        checks = [
            ("axios.defaults.xsrfCookieName = 'csrftoken'", "CSRF Cookie名称配置"),
            ("axios.defaults.xsrfHeaderName = 'X-CSRFToken'", "CSRF Header名称配置"),
            ("axios.interceptors.request.use", "请求拦截器配置"),
            ("getCookie('csrftoken')", "Cookie获取函数")
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ 缺少 {description}")
                all_passed = False
                
        return all_passed
    else:
        print("❌ 前端配置文件不存在")
        return False

def test_user_model():
    """测试用户模型是否正常"""
    print("\n=== 测试用户模型 ===")
    
    try:
        # 创建测试用户
        user = User.objects.create_user(
            username='test_csrf_user',
            email='test@example.com',
            password='testpass123'
        )
        
        # 创建用户资料
        profile = UserProfile.objects.create(
            user=user,
            nickname='测试用户',
            phone='13800138000',
            gender='男',
            city='深圳'
        )
        
        print("✅ 用户模型创建成功")
        print(f"用户ID: {user.id}")
        print(f"用户名: {user.username}")
        print(f"昵称: {profile.nickname}")
        
        # 清理测试数据
        profile.delete()
        user.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ 用户模型测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试CSRF修复...")
    
    results = []
    
    # 运行各项测试
    results.append(test_csrf_exempt_decorator())
    results.append(test_frontend_config())
    results.append(test_user_model())
    
    # 输出总结
    print("\n" + "="*50)
    print("测试结果总结:")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有测试通过 ({passed}/{total})")
        print("CSRF修复已完成，用户可以正常提交个人信息修改")
    else:
        print(f"⚠️  部分测试失败 ({passed}/{total})")
        print("请检查相关配置")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)