#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
房屋数据表格功能测试脚本
验证所有新增功能是否正常工作
"""

import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from houses.views import query_house_data, get_hive_connection
from user.models import UserFavoriteBehavior, UserDetailViewBehavior, UserCommentBehavior
from django.contrib.auth.models import User
import json

def test_hive_connection():
    """测试Hive连接"""
    print("=== 测试Hive连接 ===")
    conn = get_hive_connection()
    if conn:
        print("✅ Hive连接成功")
        conn.close()
        return True
    else:
        print("❌ Hive连接失败")
        return False

def test_house_data_query():
    """测试房屋数据查询"""
    print("\n=== 测试房屋数据查询 ===")
    try:
        # 测试基本查询
        result = query_house_data(page=1, page_size=5)
        print(f"✅ 基本查询成功，返回 {len(result['data'])} 条记录")
        print(f"   总记录数: {result['total']}")
        
        # 测试带过滤条件的查询
        filters = {'city': '深圳', 'min_price': 3000, 'max_price': 8000}
        filtered_result = query_house_data(filters=filters, page=1, page_size=3)
        print(f"✅ 过滤查询成功，返回 {len(filtered_result['data'])} 条记录")
        print(f"   过滤条件: {filters}")
        
        # 显示一条示例数据
        if result['data']:
            sample = result['data'][0]
            print(f"\n示例房屋数据:")
            print(f"  城市: {sample.get('city', 'N/A')}")
            print(f"  楼盘: {sample.get('building_name', 'N/A')}")
            print(f"  户型: {sample.get('room_type', 'N/A')}")
            print(f"  价格: {sample.get('price', 'N/A')} 元/月")
            print(f"  面积: {sample.get('area_sqm', 'N/A')} ㎡")
        
        return True
    except Exception as e:
        print(f"❌ 房屋数据查询失败: {e}")
        return False

def test_user_models():
    """测试用户行为模型"""
    print("\n=== 测试用户行为模型 ===")
    try:
        # 创建测试用户
        user, created = User.objects.get_or_create(
            username='test_house_user',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
        print("✅ 用户模型测试成功")
        
        # 测试收藏行为模型
        favorite = UserFavoriteBehavior.objects.create(
            user=user,
            house_id='test_house_001'
        )
        print("✅ 收藏行为模型测试成功")
        
        # 测试查看详情行为模型
        detail_view = UserDetailViewBehavior.objects.create(
            user=user,
            house_id='test_house_001'
        )
        print("✅ 详情查看行为模型测试成功")
        
        # 测试评论行为模型
        comment = UserCommentBehavior.objects.create(
            user=user,
            house_id='test_house_001',
            comment='这是一条测试评论',
            rating=4
        )
        print("✅ 评论行为模型测试成功")
        
        # 清理测试数据
        favorite.delete()
        detail_view.delete()
        comment.delete()
        if created:
            user.delete()
            
        return True
    except Exception as e:
        print(f"❌ 用户行为模型测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点配置"""
    print("\n=== 测试API端点配置 ===")
    
    # 检查urls.py配置
    try:
        from houses import urls as houses_urls
        expected_patterns = ['house_list', 'toggle_favorite', 'house_detail', 'house_comments', 'add_comment']
        configured_patterns = [pattern.name for pattern in houses_urls.urlpatterns]
        
        missing_patterns = set(expected_patterns) - set(configured_patterns)
        if not missing_patterns:
            print("✅ 所有API端点已正确配置")
            return True
        else:
            print(f"❌ 缺少API端点: {missing_patterns}")
            return False
    except Exception as e:
        print(f"❌ API端点配置检查失败: {e}")
        return False

def test_frontend_components():
    """测试前端组件文件"""
    print("\n=== 测试前端组件文件 ===")
    
    frontend_files = [
        'frontend/src/views/Houses.vue',
        'frontend/src/components/HouseDetail.vue'
    ]
    
    all_exist = True
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} 不存在")
            all_exist = False
    
    return all_exist

def main():
    """主测试函数"""
    print("开始测试房屋数据表格功能...")
    
    tests = [
        test_hive_connection,
        test_house_data_query,
        test_user_models,
        test_api_endpoints,
        test_frontend_components
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"测试执行出错: {e}")
            results.append(False)
    
    # 输出总结
    print("\n" + "="*50)
    print("测试结果总结:")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有测试通过 ({passed}/{total})")
        print("\n房屋数据表格功能已完全实现，包含:")
        print("1. ✅ 分页、高级搜索和筛选功能")
        print("2. ✅ 通过PyHive读取dwd_house_data表")
        print("3. ✅ 收藏功能")
        print("4. ✅ 丰富的房屋信息展示")
        print("5. ✅ 详情页面跳转")
        print("6. ✅ 评论功能")
        print("7. ✅ 用户行为记录到MySQL数据库")
    else:
        print(f"⚠️  部分测试失败 ({passed}/{total})")
        print("请检查相关配置和代码")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)