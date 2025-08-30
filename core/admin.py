from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# --- ADMIN REGISTRATION ---
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_seller", "is_mentor", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Roles", {"fields": ("is_seller", "is_mentor")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Roles", {"fields": ("is_seller", "is_mentor")}),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "seller", "created_at")
    search_fields = ("name", "category")
    list_filter = ("category", "created_at")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("buyer", "total_amount", "is_paid", "status", "created_at")
    list_filter = ("status", "is_paid", "created_at")
    search_fields = ("buyer__username",)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")

@admin.register(SavingsGroup)
class SavingsGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "total_savings", "created_at")

@admin.register(SavingsMember)
class SavingsMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "balance")

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("member", "amount", "interest_rate", "duration_months", "status", "requested_at", "updated_at")
    list_filter = ("status", "requested_at", "updated_at")
    search_fields = ("member__user__username",)

@admin.register(BusinessTemplate)
class BusinessTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__username")

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "skills", "availability")
    search_fields = ("skills",)

@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ("mentee", "mentor", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("mentee__username", "mentor__username")