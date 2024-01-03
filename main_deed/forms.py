from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Выбрать категорию'
        self.fields['photo'].label ='Фото < 5МБ'

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


# Формы регистрации и авторизации

class RegUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Почта',
                             widget=forms.EmailInput(attrs={'class': 'form-input', 'type':'email'}))
    date_birth = forms.DateField(label='Рождение',
                             widget=forms.DateInput(attrs={'class': 'form-input', 'type':'date',
                                                           'min': '1900-01-01'}))
    photo = forms.ImageField(label='Фото < 5МБ',
                             widget=forms.FileInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'photo', 'date_birth', 'username', 'password1', 'password2',
                  )

class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Имя',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    captcha = CaptchaField()

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    email = forms.EmailField(label='Email', max_length=100)
    content = forms.CharField(label='Сообщение', max_length=5000,
                              widget=forms.Textarea(attrs={'cols': 40, 'rows': 10})
                              )
    captcha = CaptchaField()
