from django.shortcuts import render, redirect
from django.http import HttpResponse
from gamer_view.forms import UserForm, UserProfileForm ,CategoryForm, PageForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from gamer_view.models import Category, Page, Review ,User, UserProfile
from django.contrib import messages
from django.db.models import Avg, IntegerField


# Create your views here
def home(request):
    #Get the latest added page
    page_list = Page.objects.order_by('-date_created')[:3]

    context_dict={}
    context_dict['pages']=page_list

    return render(request, 'gamer_view/home.html', context=context_dict)

def about(request):
    return render(request, 'gamer_view/about.html')


#displays all the categories
def show_categories(request):
    context_dict={}
    cat_list={}
    cats = Category.objects.all()
    for cat in cats:
        page=list(Page.objects.filter(cat=cat.category).order_by('-date_created')[:3])
        cat_list[cat]=page
    context_dict['categories']=cat_list
    return render(request, 'gamer_view/categories.html', context=context_dict)

def show_category(request, category_name):
    context_dict={}

    try:
        #Gets the category
        category = Category.objects.get(category=category_name)

        
        #Get the related pages
        pages=Page.objects.filter(cat=category)

        context_dict['pages']=pages
        context_dict['cat']=category

    except Category.DoesNotExist:
        context_dict['cat'] =None
        context_dict['pages']=None

    return render(request, 'gamer_view/category.html', context=context_dict)

def show_page(request, category_name, game):
    context_dict={}

    try:
        page = Page.objects.get(slug=game)
        reviews= list(Review.objects.filter(gamename=page).order_by('datecreated'))
        rating=getAverage(page)

        context_dict['page']=page
        context_dict['reviews']=reviews
        context_dict['rating']=rating

    except Page.DoesNotExist:
        context_dict['page']=None
        context_dict['reviews']=None
        context_dict['rating']=None

    return render(request, 'gamer_view/page.html', context=context_dict)

def trending(request):
    context_dict={}
    avg={}
    
    page_list= Page.objects.all()
    
    for game in page_list:
        avg[game]=getAverage(game)

    # removes pages that do not have reviews
    newavg=removeNull(avg)

    # Gets the top 5 rated
    top_rated_pages=sorted(newavg, key=newavg.get, reverse=True)[:5]
    
    #Get the most viewed pages
    most_viewed=Page.objects.order_by('-views')[:5]

    context_dict['top_rate_pages']=top_rated_pages
    context_dict['most_viewed']=most_viewed
    return render(request, 'gamer_view/trending.html', context=context_dict)



def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES)
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
            login(request,user)
            return redirect(reverse('gamer_view:home'))
        else:
            messages.error(request, "Username and/or password is incorrect")
            return redirect(reverse('gamer_view:login'))

    else:
        return render(request,'gamer_view/login.html')

# @login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('gamer_view:home'))


def add_category(request):
    form= CategoryForm()

    if request.method =='POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('gamer_view:show_categories')
        else:
            messages.error(request, "Field must not be empty")
            return redirect(reverse('gamer_view:add_category'))
        
    return render(request, 'gamer_view/add_category.html')

def add_page(request):
    if request.method =='POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page= form.save(commit=False)
            
            if 'image' in request.FILES:
                page.image = request.FILES['image']
                
            page.save()
            
            return redirect('gamer_view:show_page', page.cat, page.slug)
        else:
            messages.error(request, "Fields must not be empty")
            return redirect(reverse('gamer_view:add_page'))
    else:
        form=PageForm()

    return render(request, 'gamer_view/add_page.html', context={'form' :form} )
        
def myAccount(request):
    
    user= UserProfile.objects.get(user=request.user)
    Reviews= Review.objects.filter(madeby=user)
    
    return render(request, 'gamer_view/myAccount.html', context={'myReviews':Reviews})


# finds the average rating of the page and returns the integer
def getAverage(game):
    avg= Review.objects.filter(gamename=game).aggregate(Avg('rating', output_field=IntegerField()))
    average=avg['rating__avg']
    return average

# removes dictionary with null values
def removeNull(games):
    return{k:v for k, v in games.items() if v is not None}    
