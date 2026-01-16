from hdfs import InsecureClient
import os
from pathlib import Path

# 配置HDFS和Metastore参数
HDFS_HOST = os.getenv("HDFS_HOST", "http://node1:9870")
HDFS_TARGET_PATH = os.getenv("HDFS_TARGET_PATH", "/houseData/house.csv")
HDFS_USER = os.getenv("HDFS_USER", "root")

# 配置Metastore参数
METASTORE_HOST = os.getenv("METASTORE_HOST", "localhost")
METASTORE_PORT = int(os.getenv("METASTORE_PORT", "9083"))

# 项目根目录和CSV文件路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCAL_CSV_PATH = os.path.join(PROJECT_ROOT, "spider", "house.csv")


def upload_to_hdfs(local_path: str, hdfs_path: str, overwrite: bool = False) -> None:
    """上传本地CSV文件到HDFS"""
    # 检查本地文件是否存在
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"本地文件 {local_path} 不存在")

    # 创建HDFS客户端
    client = InsecureClient(HDFS_HOST, user=HDFS_USER)

    # 上传文件到HDFS
    with open(local_path, 'rb') as fp:
        client.write(hdfs_path, fp, overwrite=overwrite)

    print(f"成功上传 {local_path} 到 {hdfs_path}")


if __name__ == "__main__":
    upload_to_hdfs(LOCAL_CSV_PATH, HDFS_TARGET_PATH, overwrite=True)
