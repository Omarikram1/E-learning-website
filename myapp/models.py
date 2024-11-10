from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,  PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[('teacher', 'Teacher'), ('student', 'Student')])
    is_active = models.BooleanField(default=False)  # Set to False by default
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)  # Field for storing OTP
    otp_verified = models.BooleanField(default=False)  # Field to check if OTP is verified

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email



    # def generate_otp(self):
    #     """Generate a 6-digit OTP and store it in the user's profile."""
    #     self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    #     self.save()

    # def verify_otp(self, entered_otp):
    #     """Verify if the entered OTP matches the one stored."""
    #     return self.otp == entered_otp
    
    

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        

class Playlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')  # Field to upload video files
    title = models.CharField(max_length=200)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    duration = models.IntegerField()  # Duration in seconds

    def __str__(self):
        return f"Comment by {self.user.name} on {self.video.title}"










































































































