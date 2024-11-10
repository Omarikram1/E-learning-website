
from django.contrib import admin
from django.urls import path
from . import views
from .controllers.usercontroller import list_users,login_view,signup_view,otp_verification_view

urlpatterns = [
   
    
    path('playlist',views.playlist,name= 'playlist'),
    path('landingpage/',list_users,name= 'landingpage'),     
    path('signup',signup_view,name= 'signup_users'),  
    path('login/', login_view, name='login'),
    path('', views.home.as_view(), name='home'), 
    path('home', views.home.as_view(), name='home'), 
    path('privatedata/', views.privatedata.as_view(), name='privatedata'),
    path('otpverification/', otp_verification_view, name='otp_verification'),
]

