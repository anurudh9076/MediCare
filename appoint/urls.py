

from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home,name='home'),
    path('register/<des>',views.register,name='register'),
    path('login/<des>',views.login,name='login'),
    path('logout',views.logout,name='logout'),
      
]
