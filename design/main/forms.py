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


class AdminStatusForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'admin_comment', 'result_image']

    def clean_status(self):
        status = self.cleaned_data.get('status')

        if not self.instance or not self.instance.pk:
            return status

        current_status = self.instance.status
        if status == current_status:
            return status

        if current_status == DesignRequest.Status.NEW:
            if status != DesignRequest.Status.IN_PROGRESS:
                raise forms.ValidationError(
                    'The "New" status can only be changed to "In progress".'
                )
        elif current_status == DesignRequest.Status.IN_PROGRESS:
            if status != DesignRequest.Status.DONE:
                raise forms.ValidationError(
                    'The "In progress" status can only be changed to "Completed".'
                )
        elif current_status == DesignRequest.Status.DONE:
            raise forms.ValidationError(
                'The "Completed" status cannot be changed.'
            )

        return status

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = cleaned_data.get('admin_comment')
        image = cleaned_data.get('result_image')

        if status == 'done':
            if not comment:
                raise forms.ValidationError(
                    'When completing, you must leave a comment'
                )
            if not image:
                raise forms.ValidationError(
                    'When completing the task, you must upload a photo.'
                )

        return cleaned_data
