from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
        ('saver', 'Savings Group Member'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
    is_seller = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)  
    image = models.ImageField(upload_to='products/', blank=True, null=True) 
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name 

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem', blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class SavingsGroup(models.Model):
    name = models.CharField(max_length=100)
    total_savings = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class SavingsMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Loan(models.Model):
    member = models.ForeignKey(SavingsMember, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()
    status = models.CharField(max_length=20)
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessTemplate(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MentorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    availability = models.CharField(max_length=100)
    bio = models.TextField(blank=True)  
    expertise = models.CharField(max_length=200, blank=True)  # Add this
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)  # Add this

class MentorshipRequest(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_requests')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_requests')
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)  # ADD THIS LINE


    
    def __str__(self):
        return f"{self.user.username}'s MentorProfile"