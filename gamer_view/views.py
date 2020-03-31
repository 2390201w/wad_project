from django.shortcuts import render, redirect
from django.http import HttpResponse
from gamer_view.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login


# Create your views here
def Home(request):
    page_list = Page.objects.order_by(-'date')[:3]

    context_dict={}
    context['pages']=page_list
    return render(request, 'gamer_view/Home.html', context=context_dict)

def AboutUs (request):
    return HttpResponse(request, 'gamer_view/AboutUs.html')

def Trending(request):
    return HttpResponse(request, 'gamer_view/Trending.html')

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
                return redirect(reverse('gamer_view:Home'))
            else:
                return HttpResponse('Your gamer_view account is disabled.')
        
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'gamer_view/login.html')