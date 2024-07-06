from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model

from blog.models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.now()

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'format': '%Y-%m-%dT%H:%M'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'post', 'is_published')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'last_login')
