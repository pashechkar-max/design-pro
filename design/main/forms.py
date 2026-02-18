import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DesignRequest, Category

class RegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    patronymic = forms.CharField(required=False)
    email = forms.EmailField()
    agree = forms.BooleanField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'username',
            'email',
            'password1',
            'password2',
            'agree'
        )

    def clean_first_name(self):
        if not re.match(r'^[A-Za-zА-Яа-яЁё\- ]+$', self.cleaned_data['first_name']):
            raise forms.ValidationError("Invalid name format")
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if not re.match(r'^[A-Za-zА-Яа-яЁё\- ]+$', self.cleaned_data['last_name']):
            raise forms.ValidationError("Invalid last name format")
        return self.cleaned_data['last_name']

    def clean_username(self):
        if not re.match(r'^[A-Za-zА-Яа-яЁё\- ]+$', self.cleaned_data['username']):
            raise forms.ValidationError("Login only in Latin and hyphen")
        return self.cleaned_data['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            user.profile.patronymic = self.cleaned_data['patronymic']
            user.profile.save()

        return user


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            raise forms.ValidationError('Photo required')

        return photo

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
