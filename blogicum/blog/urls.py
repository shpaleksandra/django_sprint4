from django.urls import path

from .views import index, add_comment, get_profile, edit_profile
from .views import CategoryListView, PostDetailView, PostCreateView
from .views import PostUpdateView, CommentUpdateView, CommentDeleteView
from .views import PostsDeleteView

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),

    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),

    path('posts/create/', PostCreateView.as_view(), name='create_post'),

    path('posts/<int:post_id>/edit/', PostUpdateView.as_view(),
         name='edit_post'),

    path('posts/<int:post_id>/delete/', PostsDeleteView.as_view(),
         name='delete_post'),

    path('posts/<int:post_id>/comment/', add_comment,
         name='add_comment'),

    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         CommentUpdateView.as_view(), name='edit_comment'),

    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         CommentDeleteView.as_view(), name='delete_comment'),

    path(
        'category/<slug:category_slug>/',
        CategoryListView.as_view(),
        name='category_posts'),

    path('profile/<str:username>/', get_profile,
         name='profile'),

    path('accounts/profile/', edit_profile,
         name='profile'),

    path('edit_profile/', edit_profile, name='edit_profile'),
]
