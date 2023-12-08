from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.

class DeedArticles(models.Model):
    title = models.CharField(max_length=30, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст')
    photo = models.ImageField(upload_to="photos/%artmain/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Статья в разделе \'О нас\'"
        verbose_name_plural = "Статьи в разделе \'О нас\'"
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# AUTH_USER_MODEL = 'my_app.MyUser'в settings.py
# написан для получения слагов для авторизированного профиля
class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True,
                              null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_pk': self.pk})