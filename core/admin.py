from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Product,
    SavingsGroup, SavingsMember, Transaction,
    MentorProfile, MentorshipRequest,
    Cart, CartItem, Order
)


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


@admin.register(SavingsGroup)
class SavingsGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "total_savings")


@admin.register(SavingsMember)
class SavingsMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "balance")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "amount", "date")
    list_filter = ("date",)


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "skills", "availability")
    search_fields = ("skills",)


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ("mentee", "mentor", "status", "created_at")
    list_filter = ("status", "created_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "total_amount", "is_paid", "created_at")
    list_filter = ("is_paid", "created_at")
