from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Post, Comment
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .forms import CommentForm, PostForm, UserForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def get_posts(post_objects):
    return post_objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).annotate(comment_count=Count('comments'))


def index(request):
    post_list = get_posts(Post.objects).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_nubmer = request.GET.get('page')
    page_obj = paginator.get_page(page_nubmer)
    return render(request, 'blog/index.html', {'post_list': post_list,
                                               'page_obj': page_obj})


def filter_published(obj):
    return obj.filter(is_published=True)


def select_post_objects(obj):
    return obj.objects.select_related(
        'author',
        'location',
        'category',
    )


class PostDetailView(ListView):
    template_name = 'blog/detail.html'
    paginate_by = 10

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if self.request.user != post.author and (
            not post.is_published
            or not post.category.is_published
            or post.pub_date > timezone.now()
        ):
            raise Http404
        return post

    def get_queryset(self):
        return self.get_object().comments.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_object()
        context['comments'] = (
            self.get_object().comments.select_related('author').all()
        )
        return context


class CategoryListView(ListView):
    model = Category
    category = None
    template_name = 'blog/category.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=kwargs['category_slug'],
            is_published=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return filter_published(select_post_objects(Post).filter(
            category=self.category.id,
            pub_date__lte=timezone.now()
        )).annotate(comment_count=Count('comments')).order_by('-pub_date')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.pub_date = timezone.now()
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user.username
        return reverse('blog:profile',
                       kwargs={'username': user})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_object(self, **kwargs):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id'),
        )

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect(
                'blog:post_detail',
                self.kwargs.get('post_id')
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get('post_id')}
        )


class PostsDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'

    def get_object(self, **kwargs):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id'),
        )

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect(
                'blog:post_detail',
                self.kwargs.get('post_id')
            )
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method != 'POST':
        form = CommentForm()
        return render(request, 'blog/detail.html',
                      {'form': form, 'post': post})

    form = CommentForm(request.POST)
    if not form.is_valid():
        return render(request, 'blog/detail.html',
                      {'form': form, 'post': post})

    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.save()

    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('blog:post_detail', post_id=obj.id)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404
        return get_object_or_404(
            Comment,
            pk=self.kwargs.get('comment_id'),
            post=Post.objects.get(pk=self.kwargs.get('post_id')),
            author=self.request.user
        )

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return get_object_or_404(
            Comment,
            pk=self.kwargs.get('comment_id'),
            post=post,
            author=self.request.user)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get('post_id')}
        )


def get_profile(request, username):
    profile = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=profile).annotate(
        comment_count=Count('comments')).order_by('-pub_date')
    if not request.user.is_authenticated:
        user_posts = Post.objects.select_related('author').filter(
            pub_date__lte=timezone.now(),
            is_published=True).order_by('-pub_date')
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = UserForm(instance=request.user)
        return render(request, 'blog/user.html', {'form': form})
