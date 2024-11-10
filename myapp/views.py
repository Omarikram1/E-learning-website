from django.http import JsonResponse
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate
from myapp.forms import CustomUserCreationForm
import json
from rest_framework.response import Response
from .models import CustomUser, Course, Playlist, Video, Comment
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import random  # For generating OTP
from rest_framework.views import APIView
from django.core.mail import send_mail  # For sending email
from django.conf import settings

class privatedata(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return render(request, 'privatedata.html')


class home(APIView):
  
    def get(self, request):
       
        return render(request, 'homepage.html')
        


def playlist(request):
    return HttpResponse("This is playlist page")

