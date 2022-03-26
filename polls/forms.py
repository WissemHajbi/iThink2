from django import forms
from .models import user
from .models import poll
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class registerForm(UserCreationForm):
    
    email = forms.EmailField(max_length=255, help_text="Add a valid email adress please")
    
    class Meta:
         model = User
         fields = ["username", "email", "password1", "password2"]
         
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user_object = user.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"{email} is already in use.")
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            user_object = user.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"{username} is already in use.")

class pollForm(forms.ModelForm):
    class Meta:
        model = poll
        fields = "__all__"