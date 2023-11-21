from django.db.models import Count

from .models import *


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('deedarticles')) # изменить, сделать проверку если есть хотя бы одна статья
        context['cats'] = cats
        context['show_add_article'] = self.request.user.is_authenticated
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context