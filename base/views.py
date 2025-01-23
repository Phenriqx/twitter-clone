from django.shortcuts import render, redirect
from .models import User, Post

# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'home.html', context)

def loadPosts(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, 'posts.html', context)