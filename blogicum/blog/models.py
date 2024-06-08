from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

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


class Post(BaseBlogModel):
    title = models.CharField('Заголовок', max_length=settings.MAX_LENGTH)
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

    def __str__(self):
        return self.text[:100]

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
