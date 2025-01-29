from django.contrib import admin
from .models import Post, User, Repost, Like, Comment, Bookmark
from django.contrib.auth import get_user_model

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Repost)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Bookmark)