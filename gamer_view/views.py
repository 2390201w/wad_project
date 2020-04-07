from django.shortcuts import render, redirect
from django.http import HttpResponse
from gamer_view.forms import UserForm, UserProfileForm ,CategoryForm, PageForm, ReviewForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from gamer_view.models import Category, Page, Review ,User, UserProfile
from django.contrib import messages
from django.db.models import Avg, IntegerField

'''
    Home view:
    Displays to the user the 3 latest additions to the site 
'''
def home(request):
    
    # gets the latest added page
    page_list = Page.objects.order_by('-date_created')[:3]

    context_dict={}
    context_dict['pages']=page_list

    if request.method =='POST':
        # formats the input from user to match the slug
        name= (request.POST.get('gamename')).replace(' ' , '-').lower()

        # redirects user to game page if game entered by user exists
        try:
            page=Page.objects.filter(slug=name).values('cat_id')
            return redirect('gamer_view:show_page', page[0]['cat_id'], name)
        except:

            # error message when game does  not exist
             messages.error(request, "Game does not exist")        

    return render(request, 'gamer_view/home.html', context=context_dict)

'''
    About view:
    Displays informations about the site
'''
def about(request):
    return render(request, 'gamer_view/about.html')

'''
    Show Categories view:
    Displays all the categories in the site with thier 3 most viewed games
'''
def show_categories(request):
    context_dict={}
    cat_list={}
    cats = Category.objects.all()
    catE={}
    for cat in cats:
        # gets the games related to the category  
        page=list(Page.objects.filter(cat=cat.category).order_by('-views')[:3])
        if len(page) ==0:
            catE[cat]=page
            continue 
        # creates a dictionary entry with the name of the category as the key and the list of games as the value 
        cat_list[cat]=page
        
    for cat in catE:
        cat_list[cat]=catE[cat]
    context_dict['categories']=cat_list
    return render(request, 'gamer_view/categories.html', context=context_dict)

'''
    Show Category view:
    Displays the category and all its games
'''
def show_category(request, category_name):
    context_dict={}

    try:
        # gets the category name
        category = Category.objects.get(category=category_name)

        
        # get the related games
        pages=Page.objects.filter(cat=category)

        context_dict['pages']=pages
        context_dict['cat']=category

    except Category.DoesNotExist:
        context_dict['cat'] =None
        context_dict['pages']=None

    return render(request, 'gamer_view/category.html', context=context_dict)

'''
    Show Page view:
    Displays the game details and all its reviews 
'''
def show_page(request, category_name, game):
    context_dict={}

    try:
        page = Page.objects.get(slug=game)

        # gets the reviews for the game and sorts them in a descending order
        reviews= list(Review.objects.filter(gamename=page).order_by('-datecreated'))

        # gets the average rating for the game using the getAverage function
        rating=getAverage(page)

        context_dict['page']=page
        context_dict['reviews']=reviews
        context_dict['rating']=rating

    except Page.DoesNotExist:
        context_dict['page']=None
        context_dict['reviews']=None
        context_dict['rating']=None

    return render(request, 'gamer_view/page.html', context=context_dict)

'''
    Trending view:
    Displays the top 5 most viewed and top rated games in the site
'''
def trending(request):
    context_dict={}
    avg={}
    page_list= Page.objects.all()
    
    for game in page_list:
        
        # creates a dictionary entry with the game as the key and the average rating for the game as the value
        avg[game]=getAverage(game)

    # removes games that do not have reviews
    avg=removeNull(avg)

    # gets the top 5 rated games
    top_rated_pages=sorted(avg, key=avg.get, reverse=True)[:5]
    
    # get the 5 most viewed games
    most_viewed=Page.objects.order_by('-views')[:5]

    context_dict['top_rate_pages']=top_rated_pages
    context_dict['most_viewed']=most_viewed
    return render(request, 'gamer_view/trending.html', context=context_dict)

'''
    Register view:
    Lets users register to our site
'''
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
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'gamer_view/register.html', context = {'user_form' : user_form,
                                                                    'profile_form' : profile_form,
                                                                    'registered' : registered})
'''
    User Login view:
    Lets user login if they have an account
'''
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            login(request,user)
            return redirect(reverse('gamer_view:home'))
        else:
            
            # error message when users enter invalid details
            messages.error(request, "Username and/or password is invalid")
            return redirect(reverse('gamer_view:login'))

    else:
        return render(request,'gamer_view/login.html')
    
'''
    User Logout view:
    Lets users logout provided that they are logged in
'''
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('gamer_view:home'))

'''
    My Account view:
    Displays the user's name, profile picture, reviews made.
    can only be accessed if they are logged in
'''
@login_required
def my_account(request):
    
    user= UserProfile.objects.get(user=request.user)
    Reviews= Review.objects.filter(madeby=user)
    
    return render(request, 'gamer_view/my_account.html', context={'myReviews':Reviews,
                                                                 'user': user})
'''
    Add Category view:
    Lets users add a category provided that they are logged in
'''
@login_required
def add_category(request):
    form= CategoryForm()

    if request.method =='POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('gamer_view:show_categories')
        else:
            
            # Error message when the input is empty or the category exists
            messages.error(request, "Your entry must be non-empty and a non-existing category")
            return redirect(reverse('gamer_view:add_category'))
        
    return render(request, 'gamer_view/add_category.html')

'''
    Add Page view:
    Lets users add a game provided that they are logged in
'''
@login_required
def add_page(request):
    if request.method =='POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                page= form.save(commit=False)
                
                if 'image' in request.FILES:
                    page.image = request.FILES['image']
                    
                page.save()
                
                return redirect('gamer_view:show_page', page.cat, page.slug)
            except:
                
                # error message when user tries to add a game with empty field(s)
                messages.error(request, "Game already exising")
                return redirect(reverse('gamer_view:add_page'))
    else:
        form=PageForm()

    return render(request, 'gamer_view/add_page.html', context={'form' :form} )

'''
    Add Review view:
    Lets users add a review provided that they are logged in
'''
@login_required        
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review= form.save(commit =False)
            user=UserProfile.objects.get(user=request.user) 
            game= (request.POST.get('gamename'))
            revd=Review.objects.filter(madeby=user).values('gamename_id')
            
            for gam in revd:
                if int(gam['gamename_id']) == int(game):
                    messages.error(request, "Cannot make another review for the same game")
                    return redirect('gamer_view:add_review')

            review= form.save(commit =False)
            user=UserProfile.objects.get(user=request.user)   
            review.madeby=user
            
            review.save()
            return redirect('gamer_view:show_page', review.gamename.cat, review.gamename.slug)

    else:
        form =ReviewForm()
    return render(request, 'gamer_view/add_review.html', context={'form' :form})
'''
    Helper functions:
    getAverage- obtains the all the ratings made in the reviews for a game and calculates its average, returning the integer value
    removeNull- loops though the dictionary and adds the entries where its value is not "None"
'''

def getAverage(game):
    avg= Review.objects.filter(gamename=game).aggregate(Avg('rating'))
    if avg['rating__avg']==None:
        return avg['rating__avg']
    else:
        return round(avg['rating__avg'], 2)

def removeNull(games):
    return{k:v for k, v in games.items() if v is not None}    
