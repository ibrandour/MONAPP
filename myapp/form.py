from django import forms
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['age', 'genre', 'niveau_scolaire', 'ethnie']
