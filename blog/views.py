from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import PostForm, UserForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{'post': post})

@login_required
def post_new(request):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')

    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', pk=post.pk)

        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        post = get_object_or_404(Post, pk = pk)
        post.publish()
        return redirect('post_detail', pk = pk)

@login_required
def post_remove(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')

#@login_required
def logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    #print("Hello")
    return render(request, 'blog/login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'blog/post_list.html', {'posts': posts})
            else:
                return render(request, 'blog/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'blog/login.html', {'error_message': 'Invalid login'})
    return render(request, 'blog/login.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'blog/post_list.html', {'posts': posts})
    context = {
        "form": form,
    }
    return render(request, 'blog/register.html', context)
