from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/<str:pk>', views.loadPosts, name='posts')
]
