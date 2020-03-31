from django.shortcuts import render
from django.http import HttpResponse


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
