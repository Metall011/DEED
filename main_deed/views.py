from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *


def index(request):

    context = {
        'title': 'DEED',
    }

    return render(request, 'main_deed/main_deed.html', context=context)


class AboutArticles(DataMixin, ListView):
    model = DeedArticles
    template_name = 'main_deed/about.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О проекте')
        return {**context, **c_def}

    def get_queryset(self):
        return self.model.objects.filter(is_published=True).select_related('cat')


class CategoryArticles(DataMixin, ListView):
    model = DeedArticles
    template_name = 'main_deed/about.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=str(c.name),
                                      cat_selected=c.pk,
                                      )

        return {**context, **c_def}

    def get_queryset(self):
        return self.model.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                         is_published=True
                                         ).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = DeedArticles
    template_name = 'main_deed/article.html'
    context_object_name = 'article'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        articles = list(self.model.objects.filter(is_published=True))
        art_index = articles.index(self.model.objects.filter(slug=self.kwargs['post_slug'])[0])
        near_articles = {'last': None if art_index == len(articles)-1 else articles[art_index+1],
                        'next': None if art_index == 0 else articles[art_index-1]
                        }

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['article'],
                                      near_articles=near_articles,
                                      )
        return {**context, **c_def}

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)


class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    model = DeedArticles
    form_class = AddPostForm
    template_name = 'main_deed/addarticle.html'
    success_url = reverse_lazy('about')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return {**context, **c_def}

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



# Авторизация и регистрация пользователя

class RegUser(DataMixin, CreateView):
    form_class = RegUserForm
    template_name = 'main_deed/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')

class LoginUser(DataMixin, LoginView):
    form_class = AuthForm
    template_name = 'main_deed/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('login')

class ShowProfile(DetailView):
    model = User
    template_name = 'main_deed/profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['user_pk'])

def pageNotFound(request, exception):
    return redirect('main', permanent=True)

