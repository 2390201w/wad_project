from django import forms
from gamer_view.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:205px'
            }
        )                       
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:287px'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:211px'
            }
        )                       
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        help_texts = {
            'username': None,
        }

class UserProfileForm(forms.ModelForm):
    
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px;'
            }
        )
    )
    
    class Meta:
        model = UserProfile
        fields = ('picture',)
