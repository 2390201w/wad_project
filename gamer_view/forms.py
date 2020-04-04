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
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:210px'
            }
        )
    )
    
    class Meta:
        model = UserProfile
        fields = ('picture',)

class CategoryForm(forms.ModelForm):
    
    category=forms.CharField(max_length=30, required=True)

    class Meta:
        model =Category
        fields=('category',)


class PageForm(forms.ModelForm):
    gamename= forms.CharField(max_length=30, label="Game Name", required=True)
    cat=forms.ModelChoiceField(queryset=Category.objects.all(),label="Category", required=True)
    description=forms.CharField(max_length=500, required=True)
    image= forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:210px'
            }
        ),required=True)
    views=forms.IntegerField(widget=forms.HiddenInput(), initial=1)
        
    class Meta:
        model =Page
        fields=('gamename','cat','description', 'image', 'views',)
