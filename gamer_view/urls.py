from django.urls import path
from gamer_view import views

app_name = 'gamer_view'

urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('categories/', views.show_categories, name ='show_categories'),
path('categories/<category_name>/', views.show_category, name='show_category'),
path('categories/<category_name>/<slug:game>/', views.show_page, name='show_page'),
path('add_category/', views.add_category, name='add_category'),
path('add_page/', views.add_page, name='add_page'),
path('add_review/', views.add_review, name='add_review'),
path('trending/', views.trending, name='trending'),
path('register/',views.register, name='register'),
path('login/',views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('my_account/', views.my_account, name='my_account'),
]

