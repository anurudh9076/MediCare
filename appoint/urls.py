

from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home,name='home'),
    path('search_doctors',views.search_doctors,name='search-doctors'),
    path('register/<des>',views.register,name='register'),
    path('login/<des>',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('doctor_profile',views.doctor_profile,name='doctor-profile'),
    path('make_appointment/<doctor_id>',views.make_appointment,name='make-appointment'),
    path('appoint',views.appoint,name='appoint'),
    path('view_appointments',views.view_appointments,name='view-appointments'),
    path('cancel_appointment/<app_id>',views.cancel_appointment,name='cancel-appointment'),
    path('done_appointment/<app_id>',views.done_appointment,name='done-appointment'),
    path('view_profile',views.view_profile,name='view-profile'),

   
]

