from django.shortcuts import get_object_or_404, render
from .models import Category, Post
from django.utils import timezone


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    posts = Post.objects.filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True
    )
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, 'blog/category.html', context)
