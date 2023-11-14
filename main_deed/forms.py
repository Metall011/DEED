from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Выбрать категорию'

    class Meta:
        model = DeedArticles
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 30:
            raise ValidationError('Длина превышает 30 символов')
        return title

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if len(slug) > 255:
            raise ValidationError('Длина превышает 255 символов')
        return slug