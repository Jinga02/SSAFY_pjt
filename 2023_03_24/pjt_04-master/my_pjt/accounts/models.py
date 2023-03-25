from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):   # AbstractUser는 django에서 기본적으로 제공되는 로그인 기능을 수정하는 것
    pass