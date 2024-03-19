from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'example', 'class': "form-control"}),
                               max_length=250)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'example1945@gmail.com', 'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': "form-control"}))
    password2 = forms.CharField(label='confirm password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': "form-control"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this is email already exist')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this is username already taken')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords dont match')


class LoginForm(forms.Form):
    username = forms.CharField(label='email or username',
                               widget=forms.TextInput(attrs={'placeholder': 'example', 'class': "form-control"}),
                               max_length=250)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': "form-control"}))


class UserProfileEditForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control"}))

    class Meta:
        model = Profile
        fields = ('biography',)
        widgets = {
            'biography': forms.Textarea(attrs={'class': "form-control"})
        }
