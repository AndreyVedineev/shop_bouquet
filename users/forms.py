from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from shop.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', "password1", 'password2', 'phone', 'country', 'avatar')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['password'].widget = forms.HiddenInput()


class UserKeyForm(StyleFormMixin, forms.Form):
    verification_key = forms.CharField(max_length=6, label='ключ')

