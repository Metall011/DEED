from django.db.models import Count
from django.core.cache import cache

from .models import *


class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs

        # кэширование данных и проверка на кэширование
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('deedarticles'))
            cache.set('cats', cats, 60)

        context['cats'] = cats
        context['show_add_article'] = self.request.user.is_authenticated
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context