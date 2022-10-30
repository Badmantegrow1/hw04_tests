from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post, Group


User = get_user_model()


NUMBER_OF_POSTS: int = 10


def paginator(request, post_list):
    p = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.select_related('author').all()
    context = {
        'page_obj': paginator(request, post_list)
    }
    return render(request, 'posts/index.html', context)


def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts_group.all()
    context = {
        'page_obj': paginator(request, post_list),
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts_author.all()
    context = {
        'username': user,
        'page_obj': paginator(request, post_list),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def post_create(request):
    is_edit = False
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': is_edit})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if post.author != request.user:
        return redirect('posts:post_detail', post.pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post.pk)
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': is_edit, 'post': post})
