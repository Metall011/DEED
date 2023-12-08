from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class DeedArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(DeedArticles, DeedArticlesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)