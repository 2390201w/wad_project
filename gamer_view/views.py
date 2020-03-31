from django.shortcuts import render
from django.http import HttpResponse


# Create your views here
def Home(request):
    return render(request, 'gamer_view/Home.html')

def AboutUs (request):
    return HttpResponse(request, 'gamer_view/AboutUs.html')

def Trending(request):
    return HttpResponse(request, 'gamer_view/Trending.html')
