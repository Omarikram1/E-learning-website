
# user_controller.py
import logging
from urllib import response

logger = logging.getLogger(__name__)
import random
from tokenize import Comment
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from yaml import serialize
from myapp.forms import CustomUserCreationForm
# from myapp.models import CustomUser
from ..models import Course, CustomUser, Playlist, Video
import json
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login


def list_users(request):
    users = CustomUser.objects.all()
    courses = Course.objects.all()
    playlists = Playlist.objects.all()
    videos = Video.objects.all()
    # comments = Comment.objects.all()

    context = {
        'users': users,
        'courses': courses,
        'playlists': playlists,
        'videos': videos,
        'comments': 0,
    }
    return render(request, "projectmodelsinfo.html", context)




@api_view(['GET', 'POST'])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)  # Correct way to handle JSON in Django
            email = data.get('email')
            password = data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                global ACCESS_TOKEN_GLOBAL
                ACCESS_TOKEN_GLOBAL=str(refresh.access_token)


                response = Response({
                    'success': True,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })

                # response.set_cookie('Access_Token', str(refresh.access_token), httponly=True)
                # response.set_cookie('Refresh_Token', str(refresh), httponly=True)
                response.set_cookie('logged_in', True)
                response.set_cookie('Access_Token', str(refresh.access_token))
                response.set_cookie('Refresh_Token', str(refresh))

                
                # response = HttpResponseRedirect('/home')  # Redirect to the homepage
                return response
            else:
                return Response({'success': False, 'message': 'Invalid credentials'}, status=400)
        except Exception as e:
            logger.error(f"Error in login_view: {e}")
            return Response({'success': False, 'message': 'hello world'+str(e)}, status=500)

    return Response({'success': False, 'message': 'Method not allowed'}, status=405)





#model me ghusana ha isse

class loginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()




#helper function
def generate_otp():
    """ Generate a 6-digit OTP """
    return random.randint(100000, 999999)
# @csrf_exempt # type: ignore





@api_view(['GET', 'POST'])
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Check if a user already exists with the same email and is active
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email, is_active=True).exists():
                return render(request, 'signup.html', {'form': form, 'error': 'User with this email already exists.'})
            

            
            # Generate OTP and store user data in session
            otp = generate_otp()
            user_data = {
                'email': form.cleaned_data['email'],
                'name': form.cleaned_data['name'],
                'role': form.cleaned_data['role'],
                'password': form.cleaned_data['password1'],  # Temporarily store password
                'otp': otp
            }
            request.session['temp_user_data'] = user_data  # Store user data in session

            # Send OTP email
            subject = 'Your OTP Verification Code'
            message = f'Hello {user_data["name"]},\n\nYour OTP code is {otp}. Please enter this to verify your email.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_data['email']]
            send_mail(subject, message, email_from, recipient_list)

            return redirect('otp_verification')  # Redirect to OTP verification
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Form is invalid.'})

    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def otp_verification_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        temp_user_data = request.session.get('temp_user_data')  # Get the user data from session


        
        if temp_user_data and entered_otp == str(temp_user_data['otp']):
            # Create and save the user only after OTP verification
            user = CustomUser.objects.create_user(
                email=temp_user_data['email'],
                name=temp_user_data['name'],
                role=temp_user_data['role'],
                password=temp_user_data['password']
            )
            user.is_active = True  # Activate the user
            user.save()

            # Log the user in
            login(request, user)
            request.session.set_expiry(86400) 
            # Clean up the session data after successful OTP verification
            return redirect('home')
        else:
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP. Please try again.'})

    return render(request, 'otp_verification.html')



