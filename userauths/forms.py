from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

USER_TYPE = (
("Dcoctor", "Доктор"),
("Patient", "Пациент"),
)   

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'}))
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '**********'}))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '**********'}))
    user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={'class': 'form-control'}))   
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'full_name', 'user_type']

class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ivan@Ivan.com'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '**********'}))

    class Meta:
        model = User
        fields = ['email', 'password']
