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

class CategoryForm(forms.ModelForm):
    category=forms.CharField(max_length=30, required=True)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model =Category
        fields=('category',)


class PageForm(forms.ModelForm):
    gamename= forms.CharField(max_length=30)
    image= forms.ImageField(widget=forms.FileInput())
    views=forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    cat=forms.ModelChoiceField(queryset=Category.objects.all())
    
    class Meta:
        model =Page
        fields=('gamename', 'image', 'views', 'cat',)

       
