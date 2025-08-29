from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Product, SavingsGroup,MentorshipRequest, MentorProfile

User = get_user_model()

from .models import MentorProfile

class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = ["bio", "expertise", "profile_photo"]



# --- Signup Form ---
class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
        ('saver', 'Saver'),
    ]
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


# --- Login Form ---
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)


# --- Product Form ---
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "description", "image"]


# --- Savings Group Form ---
class SavingsGroupForm(forms.ModelForm):
    class Meta:
        model = SavingsGroup
        fields = ["name"]


# --- Mentor Profile Form ---
class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = ["skills", "bio", "availability"]


# --- Mentorship Request Form ---
class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a short message to the mentor..."}),
        }
