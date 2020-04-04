from django.urls import path
from gamer_view import views

app_name = 'gamer_view'

urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('categories/', views.show_categories, name ='show_categories'),
path('categories/<category_name>/', views.show_category, name='show_category'),
path('categories/<category_name>/<game>/', views.show_page, name='show_page'),
path('add_category/', views.add_category, name='add_category'),
path('trending/', views.trending, name='trending'),
path('register/',views.register, name='register'),
path('login/',views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('myAccount/', views.myAccount, name='myAccount'),
]

