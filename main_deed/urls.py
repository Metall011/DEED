from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('about', AboutArticles.as_view(), name='about'),
    path('category/<slug:cat_slug>/', CategoryArticles.as_view(), name='category'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('add_post/', cache_page(60)(AddArticle.as_view()), name='addpost'),
    path('profile/<int:user_pk>', ShowProfile.as_view(), name='profile'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegUser.as_view(), name='register'),
    path('contact/', ContactForm.as_view(), name='contact')

]