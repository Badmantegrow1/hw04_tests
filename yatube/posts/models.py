from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    objects = None
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    description = models.TextField(verbose_name='Описание', max_length=200)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    objects = None
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Введите текст поста', max_length=3000)
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='posts_author')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name='Группа',
                              help_text='Группа, к которой будет относиться '
                                        'пост',
                              related_name="posts_group", blank=True,
                              null=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:20]
