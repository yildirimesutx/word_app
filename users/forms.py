from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User # user ı kullan ve sadece username ve email aldık
        fields= ('username', 'email')