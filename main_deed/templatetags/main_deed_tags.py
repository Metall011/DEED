from django import template


from main_deed.models import *

register = template.Library()

@register.simple_tag()
def get_menu():
    menu = [
        {'title': 'DEED', 'url_name': 'main', 'src_img': 'main_deed/images/deed.png'},
        {'title': 'О НАС', 'url_name': 'about', 'src_img': 'main_deed/images/about.png'},
    ]

    return menu


@register.simple_tag()
def get_categories(sort=None):
    if not sort: return Category.objects.all()
    else: return Category.objects.order_by(sort)

# Вместо тега используем клас DataMixin
# Шаблон list_articles.html и тег не используются
# @register.inclusion_tag('main_deed/list_articles.html')
# def show_categories(sort=None, cat_selected=0):
#     cats = get_categories(sort)
#     return {'cats': cats, 'cat_selected': cat_selected}
