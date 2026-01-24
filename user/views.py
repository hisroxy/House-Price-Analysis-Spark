from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserClickBehavior, UserDetailViewBehavior, UserFavoriteBehavior, UserCommentBehavior
import json

