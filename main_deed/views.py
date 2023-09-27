from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import *

def index(request):

    context = {
        'title': 'DEED',
    }

    return render(request, 'main_deed/main_deed.html', context=context)


def about(request):
    articles = DeedArticles.objects.all()

    context = {
        'title': 'О проекте',
        'articles': articles,
        'cat_selected': 0,
    }

    return render(request, 'main_deed/about.html', context=context )


def show_category(request, cat_slug):
    category = Category.objects.filter(slug=cat_slug)[0]
    articles = DeedArticles.objects.filter(cat_id=category.pk)

    if len(articles) == 0:
        raise Http404()

    context = {
        'title': category.name,
        'articles': articles,
        'cat_selected': category.pk,
    }

    return render(request, 'main_deed/about.html', context=context)


def account_login(request):
    context = {
        'title': 'Войти',
    }

    return render(request, 'main_deed/login.html', context=context)


def show_post(request, post_slug):
    article = get_object_or_404(DeedArticles, slug=post_slug)
    count_art = len(DeedArticles.objects.all())
    number_art = DeedArticles.objects.filter(slug=post_slug)[0].pk

    near_articles = {
        'last': None if number_art == 1 else DeedArticles.objects.filter(pk=number_art-1)[0],
        'next': None if number_art == count_art else DeedArticles.objects.filter(pk=number_art+1)[0],
    }

    context = {
        'title': article.title,
        'near_articles': near_articles,
        'article': article,
    }

    return render(request, 'main_deed/аrticle.html', context=context)

def addarticle(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                DeedArticles.objects.create(**form.cleaned_data)
                return redirect('about')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()

    context = {
        'title': 'Добавление статьи',
        'form': form
    }

    return render(request, 'main_deed/addarticle.html', context=context)





def pageNotFound(request, exception):
    return redirect('main', permanent=True)

