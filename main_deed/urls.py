from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('about', AboutArticles.as_view(), name='about'),
    path('category/<slug:cat_slug>/', CategoryArticles.as_view(), name='category'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('add_post/', AddArticle.as_view(), name='addpost'),
    path('login', account_login, name='login'),

]