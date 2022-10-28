from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .constants import DISPLAYED_POSTS
from .forms import PostForm
from .models import Group, Post, User



def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, DISPLAYED_POSTS)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, DISPLAYED_POSTS)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    count = author.posts.count()
    paginator = Paginator(post_list, DISPLAYED_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'count': count,
        'username': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    pub_date = post.pub_date
    post_title = post.text[:30]
    author = post.author
    author_posts = author.posts.all().count()
    context = {
        'pub_date': pub_date,
        'post_title': post_title,
        'author': author,
        'author_posts': author_posts,
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):

    form = PostForm(request.POST  or None)

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
