from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True, label="Full Name")
    role = forms.ChoiceField(choices=[('teacher', 'Teacher'), ('student', 'Student')], required=True, label="Role")
    email = forms.EmailField(required=True, label="Email Address")  # Add email field

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'role', 'password1', 'password2']

    def save(self, commit=False):  # commit=False ensures the user is not saved immediately
        user = super().save(commit=False)  # Prevents saving
        return user  # Only return the user object without saving it



