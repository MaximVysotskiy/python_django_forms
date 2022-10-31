from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Group, Post, User
from .utils import get_page_context


def index(request):
    post = Post.objects.select_related('group')
    context = context = {
        'page_obj': get_page_context(post, request)
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    context = {
        'group': group,
        'post_list': post_list,
        'page_obj': get_page_context(post_list, request)
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    context = {
        'username': author,
        'page_obj': get_page_context(post_list, request)
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):

    form = PostForm(request.POST or None)

    if form.is_valid():

        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect('posts:profile', request.user)

    return render(
        request,
        'posts/post_create.html',
        {'form': form}
    )


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.save()
            return redirect('posts:post_detail', post_id)
        return render(
            request, 'posts/post_create.html',
            {'form': form, 'is_edit': True, 'post_id': post_id}
        )
    form = PostForm(instance=post)
    return render(
        request, 'posts/post_create.html',
        {'form': form, 'is_edit': True, 'p_id': post_id}
    )
