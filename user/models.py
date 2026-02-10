from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    用户信息模型
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('男', '男'), ('女', '女'), ('未知', '未知')], default='未知')
    city = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserClickBehavior(models.Model):
    """
    用户点击行为模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='click_behaviors')
    house_id = models.CharField(max_length=100)  # 房子ID，对应Hive中的数据
    clicked_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} clicked house {self.house_id}"


class UserDetailViewBehavior(models.Model):
    """
    用户查看房子详情行为模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='detail_view_behaviors')
    house_id = models.CharField(max_length=100)  # 房子ID，对应Hive中的数据
    viewed_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)  # 查看时长（秒）
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} viewed detail of house {self.house_id}"


class UserFavoriteBehavior(models.Model):
    """
    用户收藏房屋行为模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_behaviors')
    house_id = models.CharField(max_length=100)  # 房子ID，对应Hive中的数据
    favorited_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # 是否仍然收藏

    def __str__(self):
        return f"{self.user.username} favorited house {self.house_id}"


class UserCommentBehavior(models.Model):
    """
    用户评论房屋行为模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_behaviors')
    house_id = models.CharField(max_length=100)  # 房子ID，对应Hive中的数据
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)  # 评分（可选）

    def __str__(self):
        return f"{self.user.username} commented on house {self.house_id}"