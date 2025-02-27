from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('post/<str:author>/<str:pk>/', views.getPost, name='get-post'),
    path('add-post/', views.addPost, name='add-post'),
    path('delete-post/<str:pk>/', views.deletePost, name='delete-post'),
    path('update-post/<str:pk>/', views.updatePost, name='update-post'),
    
    path('bookmarks/', views.loadBookmarks, name='bookmarks'),
    path('add-bookmark/<str:pk>/', views.addBookmark, name='add-bookmark'),
    path('delete-bookmark/<str:pk>/', views.deleteBookmark, name='delete-bookmark'),
    
    path('<str:author>/post/<str:pk>/', views.addComment, name='add-comment'),
    path('<str:author>/delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('<str:author>/update-comment/<str:pk>/', views.updateComment, name='update-comment'),
    
    path('<str:author>/lists/', views.loadLists, name='load-lists'),
    path('lists/create/', views.createList, name='create-list'),
    path('lists/get/<str:pk>/', views.getList, name='get-list'),
    path('lists/delete/<str:pk>/', views.deleteList, name='delete-list'),
    
    path('like-post/<str:pk>/', views.likePost, name='like-post'),
    path('repost/<str:pk>/', views.repost, name='repost'),
    path('search/', views.search, name='search'),
    
    path('profile/<str:user>/', views.profile, name='profile'),
    path('link/profile/<str:username>/', views.linkProfile, name='link-profile'),
    path('update-user/<str:username>/', views.udpateProfile, name='update-profile'),
    path('load-replies/<str:username>/', views.loadReplies, name='load-replies'),
    path('load-likes/<str:username>/', views.loadLikes, name='load-likes'),
    
    path('follow/<str:user_id>/', views.followUser, name='follow'),
    path('unfollow/<str:user_id>/', views.unfollowUser, name='unfollow'),
    path('<str:username>/followers/', views.listFollowers, name='followers'),
    path('<str:username>/following/', views.listFollowing, name='following')
] 