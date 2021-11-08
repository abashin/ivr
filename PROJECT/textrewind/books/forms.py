from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: rgb(255,255,255);', 'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'background-color: rgb(255,255,255);', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'background-color: rgb(255,255,255);', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'background-color: rgb(255,255,255);', 'placeholder': 'Подтверждение пароля'}))
    help_texts = {
        'review ': ' ',
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    help_texts = {
        'review ': ' ',
    }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Аккаунт с таким email уже существует, возможно стоит восстановить пароль?')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: rgb(255,255,255);', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'background-color: rgb(255,255,255);', 'placeholder': 'Пароль'}))


