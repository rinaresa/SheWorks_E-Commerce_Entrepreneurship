from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, SavingsGroup, Mentorship

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_seller", "is_mentor", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Roles", {"fields": ("is_seller", "is_mentor")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Roles", {"fields": ("is_seller", "is_mentor")}),
    )


admin.site.unregister(Product) if admin.site.is_registered(Product) else None
admin.site.register(Product)

admin.site.register(SavingsGroup)
admin.site.register(Mentorship)
