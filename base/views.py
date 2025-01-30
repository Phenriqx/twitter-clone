from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Repost, Like, Comment, Bookmark
from .forms import CustomUserCreationForm, PostForm, CommentForm


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User not found!')
            return redirect('register')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    
    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


def registerUser(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'User registered successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed!')
            
    return render(request, 'base/register.html', {'form': form})
    
    
@login_required(login_url='register')
def home(request):
    user = request.user
    form = PostForm()
    posts = Post.objects.all()
    context = {'posts': posts, 'user': user, 'form': form}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def loadPosts(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, 'base/posts.html', context)


@login_required(login_url='login')
def addPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Failed to add post!')
            
    context = {'form': form}
    return render(request, 'base/add_post.html', context)


@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    
    if request.user != post.author:
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    
    return render(request, 'base/delete_post.html', {'post': post})


@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Failed to update post!')
            
    context = {'form': form, 'post': post}
    return render(request, 'base/update_post.html', context)


@login_required(login_url='login')
def loadBookmarks(request):
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user)
    context = {'bookmarks': bookmarks}
    return render(request, 'base/bookmarks.html', context)


@login_required(login_url='login')
def addBookmark(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    
    if Bookmark.objects.filter(user=user, post=post).exists():
        return HttpResponse('Post already exists in the bookmarks')
    
    bookmark = Bookmark()
    bookmark.user = user
    bookmark.post = post
    bookmark.save()
    messages.success(request, 'Bookmark added successfully')
    return redirect('home')


@login_required(login_url='login')
def deleteBookmark(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    
    if not Bookmark.objects.filter(user=user, post=post).exists():
        return redirect('home')
    
    Bookmark.objects.filter(user=user, post=post).delete()
    messages.success(request, 'Bookmark deleted successfully')
    
    return redirect('bookmarks')


def addComment(request, author, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    author = post.author.name
    comments = Comment.objects.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = post
            comment.content = request.POST.get('content')
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect('home')
        else:
            messages.error(request, 'Failed to add comment')
    
    context = {'user': user, 
               'author': author,
               'post': post,
               'comments': comments,
    }
    return render(request, 'base/add_comment.html', context)


def like(request):
    pass