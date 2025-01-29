from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/<str:pk>', views.loadPosts, name='posts'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('add-post', views.addPost, name='add-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('bookmarks/', views.loadBookmarks, name='bookmarks'),
    path('add-bookmark/<str:pk>', views.addBookmark, name='add-bookmark'),
] 