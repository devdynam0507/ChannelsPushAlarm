from django import forms
from django.contrib.auth import (authenticate, get_user_model)
from django.contrib.auth.models import User

User = get_user_model()

class CreateUserForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='')
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder': 'Retype-Password'}), label='')

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)

        if commit:
            user.save()
        return user

    def signup(self):
        if self.is_valid():
            return User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password2']
            )

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        # user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not longer active')

        return super(UserLoginForm, self).clean(*args, **kwargs)