import os
import django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from user.models import UserProfile

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house_price_analysis.settings')
django.setup()

def init_project():
    """
    初始化项目，创建必要的数据库表并添加初始数据
    """
    print("正在初始化项目...")

    # 执行数据库迁移
    print("正在执行数据库迁移...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])

    # 创建超级用户（如果不存在）
    if not User.objects.filter(is_superuser=True).exists():
        print("正在创建超级用户...")
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        UserProfile.objects.get_or_create(user=superuser)
        print("超级用户创建成功！用户名: admin, 密码: admin123")

    print("项目初始化完成！")

if __name__ == '__main__':
    init_project()