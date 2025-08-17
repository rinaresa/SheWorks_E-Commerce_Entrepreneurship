from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Savings Group Model
class SavingsGroup(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name="savings_groups")
    total_savings = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

# Mentorship Model
class Mentorship(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mentorships_as_mentor")
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mentorships_as_mentee")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.mentee.username} → {self.mentor.username} ({self.status})"
