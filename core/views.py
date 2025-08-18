from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import SignupForm, ProductForm
from .models import Product


def is_seller(user):
    return hasattr(user, "is_seller") and user.is_seller


# Product List + Search + Pagination
def product_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query))
    if category:
        products = products.filter(category__iexact=category)

    paginator = Paginator(products, 5)  # ✅ 5 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "products/product_list.html", {"page_obj": page_obj})


# Product Detail
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})


# Create Product (Seller only)
@login_required
@user_passes_test(is_seller)
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # ✅ handle file uploads
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form})


# Update Product (Seller only, must be owner)
@login_required
@user_passes_test(is_seller)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)  # ✅ include files
        if form.is_valid():
            form.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form})


# Delete Product (Seller only, must be owner)
@login_required
@user_passes_test(is_seller)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "products/product_confirm_delete.html", {"product": product})


# Home Page
def home(request):
    return render(request, "home.html")


# Signup
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created & logged in.")
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in.")
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


# Logout
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("login")
