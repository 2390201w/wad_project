from django.shortcuts import render, redirect
from django.http import HttpResponse
from gamer_view.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login
from gamer_view.models import Category, Page


# Create your views here
def home(request):
    #Get the latest adeed page
    page_list = Page.objects.order_by('-time_created')[:3]

    context_dict={}
    context_dict['pages']=page_list
    return render(request, 'gamer_view/home.html', context=context_dict)

def about(request):
    return render(request, 'gamer_view/about.html')

def show_category(request, category_name_slug):
    context_dict={}

    try:
        #Gets the category
        category = Category.objects.get(slug=category_name_slug)

        
        #Get the related pages
        pages=Page.objects.filter(category=category)

        context_dict['pages']=pages
        context_dict['category']=category

    except Category.DoesNotExist:
        context_dict['category'] =None
        context_dict['pages']=None

    return render(request, 'gamer_view/category.html', context=context_dict)

def show_page(request, pageName):
    context_dict={}

    try:
        page = Page.objects.get(pageName=gamename)
        reviews= Reviews.objects.filter(gamename=gamename)

        context_dict['page']=page
        context_dict['reviews']=reviews

    except Page.DoesNotExist:
        context_dict['page']=None
        context_dict['reviews']=None

    return render(request, 'gamer_view/page.html', context=context_dict)

def trending(request):
    # Get the top rated pages
    top_rated_pages= Page.object.order_by('-rate')[:5]

    #Get the most viewed pages
    most_viewed=Page.object.order_by('-view')[:5]

    context_dict['top_rate_pages']=top_rated_pages
    context_dict['most_viewed']=most_viewed
    return render(request, 'gamer_view/trending.html', context=context_dict)



def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'gamer_view/register.html', context = {'user_form' : user_form,
                                                                    'profile_form' : profile_form,
                                                                    'registered' : registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('gamer_view:home'))
            else:
                return HttpResponse('Your gamer_view account is disabled.')
        
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'gamer_view/login.html')

