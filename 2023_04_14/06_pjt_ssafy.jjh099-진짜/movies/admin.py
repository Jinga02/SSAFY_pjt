from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, Comment

# Register your models here.
admin.site.register(Movie)
admin.site.register(Comment)