from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.conf import settings
from django.utils import timezone


User = get_user_model()


class BaseBlogModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
        help_text='Если установить дату и время в будущем — можно делать '
                  'отложенные публикации.',
    )

    class Meta:
        abstract = True
        ordering = ('created_at',)


class Category(BaseBlogModel):
    title = models.CharField(
        'Заголовок',
        max_length=settings.MAX_LENGTH,
        blank=True,
    )
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseBlogModel):
    name = models.CharField('Название места', max_length=settings.MAX_LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class PublishedQuerySet(models.QuerySet):

    def filter_posts_for_publication(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def count_comments(self):
        return self.select_related(
            'category', 'location', 'author'
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class Post(BaseBlogModel):
    image = models.ImageField(
        'Фото', blank=True, upload_to='posts_images/', null=True
    )
    title = models.CharField('Заголовок', max_length=100)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата и время публикации',
                                    help_text='Если установить дату и время в'
                                    ' будущем — можно делать отложенные'
                                    ' публикации.')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    objects = PublishedQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:100]


class Comment(BaseBlogModel):

    text = models.TextField('Текст')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:100]
