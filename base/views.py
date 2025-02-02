from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Repost, Like, Comment, Bookmark, List, Topic, Message
from .forms import CustomUserCreationForm, PostForm, CommentForm, ListForm


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

def deleteComment(request, author, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)
    
    if request.method == 'POST':
        Comment.objects.filter(author=user, id=comment.id).delete()
        messages.success(request, 'Comment deleted successfully')
        return redirect('home')
    
    context = {
        'user': user,
        'author': author,
        'comment': comment,
    }
    return render(request, 'base/delete_comment.html', context)

def updateComment(request, author, pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Failed to update post!')
            
    context = {'form': form, 'post': comment}
    return render(request, 'base/update_comment.html', context)

def loadLists(request, author):
    lists = List.objects.all()[:3]
    user = request.user

    context = { 'lists': lists,
                'user': user,
    }

    return render(request, 'base/lists.html', context)

def getList(request, pk):
    list = List.objects.get(id=pk)
    list_messages = list.message_set.all()
    participants = [user for user in list.participants.all()]
    
    if request.method == 'POST':
        message = Message.objects.create(
            author = request.user,
            list = list,
            content = request.POST.get('content'),
        )
        messages.success(request, 'message added successfully')
        list.participants.add(request.user)
        return redirect('get-list', list.id)
    
    context = {
        'list': list,
        'participants': participants,
        'list_messages': list_messages,
    }
    
    return render(request, 'base/list.html', context)

def createList(request):
    form = ListForm()    
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(topic=topic_name)
        messages.success(request, f'The topic {topic} has been created')
        
        List.objects.create(
            author = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        messages.success(request, 'List created successfully')
        return redirect('home')
    
    context = {'form': form, 
               'topics': topics
    }
    return render(request, 'base/add_list.html', context)

def deleteList(request, pk):
    user = request.user
    list = List.objects.get(id=pk)
    
    if request.method == 'POST':
        List.objects.filter(author=user, id=list.id).delete()
        messages.success(request, 'List deleted successfully')
        return redirect('load-lists', author=request.user)
    
    context = {
        'user': user,
        'list': list,
    }
    return render(request, 'base/delete_list.html', context)

def like(request):
    pass