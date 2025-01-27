from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Repost, Like, Comment
from .forms import CustomUserCreationForm, PostForm

#CustomUser = get_user_model()

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
            return redirect('register')
    
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
    

def home(request):
    user = request.user
    #user = User.objects.get(name=request.POST.get('name'))
    posts = Post.objects.all()
    context = {'posts': posts, 'user': user}
    return render(request, 'base/home.html', context)

def loadPosts(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, 'base/posts.html', context)

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

def like(request):
    pass