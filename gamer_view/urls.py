from django.urls import path
from gamer_view import views

app_name = 'gamer_view'

urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
path('game/<pageName>/', views.show_page, name='show_page'),
path('trending/', views.trending, name='trending'),
path('register/',views.register, name='register'),

]

