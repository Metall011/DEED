from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('about', about, name='about'),
    path('login', account_login, name='login'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<slug:cat_slug>/', show_category, name='category'),
    path('add_post', addarticle, name='addpost' )
]