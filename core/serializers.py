from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Product, Order, BusinessTemplate, SavingsGroup,
  Loan, MentorshipRequest, MentorProfile
)

User = get_user_model()


# --- Authentication & Users ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# --- E-Commerce ---
class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "image", "seller"]


class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "buyer", "product", "quantity", "status", "created_at"]


# --- Business Toolkit ---
class BusinessTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessTemplate
        fields = ["id", "title", "file", "description"]


# --- Savings & Microfinance ---
class SavingsGroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = SavingsGroup
        fields = ["id", "name", "description", "members", "created_at"]


class ContributionSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)

    #class Meta:
       # model = Contribution
        #fields = ["id", "member", "amount", "date"]


class LoanSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "member", "amount", "status", "requested_at", "repaid_at"]


# --- Mentorship ---
class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MentorProfile
        fields = ["id", "user", "bio", "skills", "experience"]


class MentorshipRequestSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    mentor = MentorProfileSerializer(read_only=True)

    class Meta:
        model = MentorshipRequest
        fields = ["id", "buyer", "mentor", "status", "created_at"]
