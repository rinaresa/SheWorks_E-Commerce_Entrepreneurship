from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Product, SavingsGroup, Transaction, MentorshipRequest, MentorProfile

User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_seller = forms.BooleanField(required=False, label="Register as Seller")
    is_mentor = forms.BooleanField(required=False, label="Register as Mentor")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_seller", "is_mentor")


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "description", "image"]


class SavingsGroupForm(forms.ModelForm):
    class Meta:
        model = SavingsGroup
        fields = ["name"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]



class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = ["skills", "bio", "availability"]


class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a short message to the mentor..."})
        }
