@echo off
echo 开始安装房价分析系统...

echo 安装后端依赖...
pip install -r requirements.txt

echo 初始化Django项目...
python init_project.py

echo 后端安装完成！
echo 要启动后端服务，请运行: python manage.py runserver
echo.
echo 前端项目结构已创建。
echo 要安装前端依赖，请进入frontend目录并运行: npm install
echo 要启动前端开发服务器，请运行: npm run dev
echo.
echo 项目启动成功！
pause