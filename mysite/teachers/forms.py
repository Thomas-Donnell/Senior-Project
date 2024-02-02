from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyClass

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email'}),
            'password1': forms.PasswordInput(render_value=True, attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm your password'}),
        }

class MyClassForm(forms.ModelForm):
    class Meta:
        model = MyClass
        fields = ['class_name', 'class_descriptor']

class EnrollForm(forms.Form):
    enrolled_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
        