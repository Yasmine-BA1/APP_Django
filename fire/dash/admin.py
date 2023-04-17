from django.contrib import admin
from .models import Post

#This makes the Post model visible in the Django admin site (can edit delete ... users with permission)
admin.site.register(Post)