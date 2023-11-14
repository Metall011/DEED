from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .models import *
from .forms import *


def index(request):

    context = {
        'title': 'DEED',
    }

    return render(request, 'main_deed/main_deed.html', context=context)


class AboutArticles(ListView):
    model = DeedArticles
    template_name = 'main_deed/about.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)


class CategoryArticles(ListView):
    model = DeedArticles
    template_name = 'main_deed/about.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['articles'][0].cat)
        context['cat_selected'] = context['articles'][0].cat_id
        return context

    def get_queryset(self):
        return self.model.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class ShowPost(DetailView):
    model = DeedArticles
    template_name = 'main_deed/article.html'
    context_object_name = 'article'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        articles = list(self.model.objects.filter(is_published=True))
        art_index = articles.index(self.model.objects.filter(slug=self.kwargs['post_slug'])[0])
        near_articles = {
        'last': None if art_index == len(articles)-1 else articles[art_index+1],
        'next': None if art_index == 0 else articles[art_index-1],
        }

        context = super().get_context_data(**kwargs)
        context['title'] = context['article']
        context['near_articles'] = near_articles

        return context

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)



class AddArticle(CreateView):
    model = DeedArticles
    form_class = AddPostForm
    template_name = 'main_deed/addarticle.html'
    success_url = reverse_lazy('about')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context




# def addarticle(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('about')
#             form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#
#     context = {
#         'title': 'Добавление статьи',
#         'form': form
#     }
#
#     return render(request, 'main_deed/addarticle.html', context=context)


def account_login(request):
    context = {
        'title': 'Войти',
    }

    return render(request, 'main_deed/login.html', context=context)


def pageNotFound(request, exception):
    return redirect('main', permanent=True)

