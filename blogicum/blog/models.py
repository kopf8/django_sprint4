from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.utils import timezone

User = get_user_model()


class BaseModel(models.Model):
    """Base class for all models."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    """Category model."""

    title = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Returns the category name."""
        return self.title


class Location(BaseModel):
    """Location model."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """Returns the location name."""
        return self.name


class PostQuerySet(models.QuerySet):
    """Selects all related objects."""

    def with_related_data(self):
        return (
            self.select_related('author', 'location', 'category')
            .all()
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )

    def published(self):
        """
        Returns all published posts in published category with published
        date not in the future.
        """
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))


class PublishedPostManager(models.Manager):
    """
    Uses QuerySet to get all published posts and display count of published
    comments for the post.
    """

    def get_queryset(self) -> PostQuerySet:
        return (
            PostQuerySet(self.model)
            .with_related_data()
            .published()
        )


class Post(BaseModel):
    """Post model."""

    title = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        )
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    objects = PostQuerySet.as_manager()
    published = PublishedPostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        """Returns the post title."""
        return self.title


class Comment(models.Model):
    """Comment model."""

    objects = None
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        """Returns the comment text."""
        return self.text
