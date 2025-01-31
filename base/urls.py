from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('posts/<str:pk>', views.loadPosts, name='posts'),
    path('add-post', views.addPost, name='add-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('update-post/<str:pk>', views.updatePost, name='update-post'),
    
    path('bookmarks/', views.loadBookmarks, name='bookmarks'),
    path('add-bookmark/<str:pk>', views.addBookmark, name='add-bookmark'),
    path('delete-bookmark/<str:pk>', views.deleteBookmark, name='delete-bookmark'),
    
    path('<str:author>/post/<str:pk>', views.addComment, name='add-comment'),
    path('<str:author>/delete-comment/<str:pk>', views.deleteComment, name='delete-comment'),
    path('<str:author>/update-comment/<str:pk>', views.updateComment, name='update-comment'),
] 