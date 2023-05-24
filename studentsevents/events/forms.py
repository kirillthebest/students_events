from django import forms
from django.forms import PasswordInput

from events.models import ProfileEvent


# форма авторизации
class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, required=True, label='Никнейм')
    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')


class DocumentForm(forms.ModelForm):
    class Meta:
        model = ProfileEvent
        fields = ('document', )