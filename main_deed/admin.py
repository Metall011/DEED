from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

from django.utils.translation import gettext_lazy as _

class ShowPhotoMixin:
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'

# Register your models here.

class DeedArticlesAdmin(admin.ModelAdmin, ShowPhotoMixin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('time_create', 'time_update', 'get_html_photo'
                       )
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo',
              'is_published', 'time_create', 'time_update'
              )
    save_on_top = True


class UserAdmin(BaseUserAdmin, ShowPhotoMixin):
    list_display = ('id', 'username', 'get_html_photo', 'first_name', 'last_name', 'is_staff',)
    list_display_links = ('id', 'username')
    fieldsets = (
        (None, {"fields": ("username", "password", "get_html_photo", "photo")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "date_birth")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ('get_html_photo', 'date_joined', 'last_login')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(DeedArticles, DeedArticlesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)

admin.site.site_title = 'Администрирование DEED'
admin.site.site_header = 'Администрирование DEED'
