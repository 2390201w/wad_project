from django.urls import path
from gamer_view import views

app_name = 'gamer_view'

urlpatterns = [
path('', views.Home, name='Home'),
path('AboutUs/', views.AboutUs, name='AboutUs'),
path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
path('game/<pageName>/', views.show_page, name='show_page'),
path('trending/', views.Trending, name='Trending'),
path('register/',views.register, name='register'),

]

