from django import forms
from gamer_view.models import Page, Category, UserProfile, Review
from django.contrib.auth.models import User

Min=6
Max=30

class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:205px'
            }
        ), min_length=Min, max_length=Max,required=True,
        error_messages={
            'min_length': 'Choose a username between 6-30 characters',
            'max_length': 'Choose a username between 6-30 characters'
        }                  
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:287px'
            }
        ),
        error_messages={'invalid': 'Invalid email Address'}
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'style': 'height:22.5px; position:relative; top:-6px; font-size:16px; width:211px'
            }
        ), min_length=Min, max_length=Max,required=True,
        error_messages={
            'min_length': 'Choose a password between 6-30 characters',
            'max_length': 'Choose a password between 6-30 characters'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


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
    slug= forms.CharField(widget=forms.HiddenInput(), required=False)
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

class ReviewForm(forms.ModelForm):
    gamename=forms.ModelChoiceField(queryset=Page.objects.all(),label="Game Name", required=True,
        widget=forms.Select(
            attrs={
                'style': 'height:30px; position:relative; top:-7px;'
            }
        )
    )
    review=forms.CharField(max_length=500, label="Review",
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'cols': 40,
                'style': 'height:150px; width: 500px; position:relative; top: 70px; font-size: 14px; padding:0.5%; margin-top:-90px'
            }
        )
    )
    rating=forms.IntegerField(widget=forms.HiddenInput(),initial=1)

    class Meta:
        model= Review
        fields=('gamename','review', 'rating',)

class SearchForm(forms.ModelForm):
    gamename=forms.CharField(max_length=30)

    class Meta:
        model = Page
        fields=('gamename',)
