from django.db import models
from django.conf import settings
# Create your models here.
class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # user확인을 위한 외래키
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes") # 좋아요 구현
    dislike_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislikes')#싫어요 구현
    title = models.CharField(max_length=20) # 영화제목
    audience = models.IntegerField()    # 관객 수
    release_date = models.DateTimeField(auto_now=True)  # 개봉일
    genre = models.CharField(max_length=30) # 장르
    score = models.FloatField() #   평점
    poster_url = models.CharField(max_length=50)    # 포스터 경로
    description = models.TextField()    # 줄거리
    actor_image = models.ImageField(blank=True, null=True) # 대표 배우 이미지

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.content