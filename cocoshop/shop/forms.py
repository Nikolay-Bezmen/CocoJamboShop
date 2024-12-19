# shop/forms.py

from django import forms
from .models import User, Products
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_password_confirm(self):
    #     password = self.cleaned_data.get("password")
    #     password_confirm = self.cleaned_data.get("password_confirm")
    #     if password and password_confirm and password != password_confirm:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password_confirm
    #
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'stock', 'category', 'brand', 'image_url']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
