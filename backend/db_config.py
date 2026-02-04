import pymysql

pymysql.install_as_MySQLdb()

# Hive配置 - 使用CUSTOM模式和密码
HIVE_CONFIG = {
    'host': '192.168.96.130',
    'port': 10000,
    'username': 'root',
    'password': 'rootcai123',  # 添加密码
    'database': 'default',
    'auth': 'CUSTOM'  # 改为CUSTOM模式
}