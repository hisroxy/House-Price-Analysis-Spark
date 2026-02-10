import os
import django

# 必须在导入任何Django模块之前设置环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# 现在可以安全导入Django模块
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from user.models import UserProfile

def init_project():
    """
    初始化项目，创建必要的数据库表并添加初始数据
    """
    print("正在初始化项目...")

    # 执行数据库迁移
    print("正在执行数据库迁移...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("数据库迁移完成！")
    except Exception as e:
        print(f"数据库迁移失败: {e}")
        return

    # 创建超级用户（如果不存在）
    try:
        if not User.objects.filter(is_superuser=True).exists():
            print("正在创建超级用户...")
            superuser = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            # 先创建UserProfile对象
            profile, created = UserProfile.objects.get_or_create(user=superuser)
            if created:
                print("超级用户及用户资料创建成功！")
            else:
                print("超级用户已存在！")
            print("超级用户创建成功！用户名: admin, 密码: admin123")
        else:
            print("超级用户已存在！")
    except Exception as e:
        print(f"创建超级用户失败: {e}")

    print("项目初始化完成！")

if __name__ == '__main__':
    init_project()