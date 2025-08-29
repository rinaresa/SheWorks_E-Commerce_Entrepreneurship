from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .models import Product, Cart, CartItem

from rest_framework import generics, permissions

from .forms import (
    SignUpForm, ProductForm, SavingsGroupForm,
 MentorProfileForm, MentorshipRequestForm
)
from .models import (
    User,  Product, Cart, CartItem, Order,
    BusinessTemplate, SavingsGroup, SavingsMember, Loan, MentorProfile, MentorshipRequest
)
from .serializers import (
    UserSerializer, ProductSerializer, OrderSerializer,
    BusinessTemplateSerializer, SavingsGroupSerializer, LoanSerializer,
    MentorProfileSerializer, MentorshipRequestSerializer
)

User = get_user_model()
def home(request):
    return render(request, 'home.html')

def community(request):
    return render(request, 'core/community.html')

def opportunities(request):
    return render(request, 'core/opportunities.html')

def about(request):
    return render(request, 'core/about.html')

# REMOVE THIS DUPLICATE FUNCTION (lines 47-58)
# @login_required
# def buyer_dashboard(request):
#     # Get all products
#     products = Product.objects.all()
#     
#     # Get or create cart for the current user
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     
#     # Count cart items
#     cart_items_count = CartItem.objects.filter(cart=cart).count()
#     
#     context = {
#         'products': products,
#         'cart_items_count': cart_items_count,
#     }
#     return render(request, 'core/dashboards/buyer_dashboard.html', context)

def seller_dashboard(request):
    return render(request, 'core/dashboards/seller_dashboard.html')

def mentor_dashboard(request):
    return render(request, 'core/dashboards/mentor_dashboard.html')

def mentee_dashboard(request):
    return render(request, 'core/dashboards/mentee_dashboard.html')


# --- Authentication & Users ---
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- E-Commerce ---
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- Business Toolkit ---
class BusinessTemplateListView(generics.ListAPIView):
    queryset = BusinessTemplate.objects.all()
    serializer_class = BusinessTemplateSerializer
    permission_classes = [permissions.AllowAny]

# --- Savings & Microfinance ---
class SavingsGroupListCreateView(generics.ListCreateAPIView):
    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class SavingsGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

#class ContributionListCreateView(generics.ListCreateAPIView):
   # queryset = Contribution.objects.all()
  #  serializer_class = ContributionSerializer
   # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)

# --- Mentorship ---
class MentorProfileListCreateView(generics.ListCreateAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MentorProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MentorshipRequestListCreateView(generics.ListCreateAPIView):
    queryset = MentorshipRequest.objects.all()
    serializer_class = MentorshipRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(mentee=self.request.user)

# ------------------ Web Views ------------------

# --- Authentication ---
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get("role")
            user.save()
            Profile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, "Account created & logged in.")
            return redirect("post_login_redirect")
    else:
        form = SignUpForm()
    return render(request, "core/auth/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in.")
            return redirect("post_login_redirect")
    else:
        form = AuthenticationForm()
    return render(request, "core/auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("login")

@login_required
def post_login_redirect(request):
    role = getattr(request.user.profile, "role", None)
    if role == "buyer":
        return redirect("buyer_dashboard")
    return redirect("dashboard")

# --- Dashboards ---
@login_required
def dashboard(request):
    user = request.user
    context = {}
    role = getattr(user.profile, "role", None)
    
    if role == "seller":
        context["products"] = user.products.all()
        return render(request, "dashboards/seller_dashboard.html", context)
    
    elif role == "mentor":
        context["requests"] = user.received_requests.all()
        return render(request, "dashboards/mentor_dashboard.html", context)
    
    return render(request, "home.html")

@login_required
def buyer_dashboard(request):
    products = Product.objects.all()
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    return render(request, "dashboards/buyer_dashboard.html", {
        "products": products,
        "cart_items_count": cart_items_count
    })

# --- Products ---
def product_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__iexact=category)
    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "products/product_list.html", {"page_obj": page_obj})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})

@login_required
@user_passes_test(lambda u: getattr(u.profile, "role", "")=="seller")
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form})

@login_required
@user_passes_test(lambda u: getattr(u.profile, "role", "")=="seller")
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form})

@login_required
@user_passes_test(lambda u: getattr(u.profile, "role", "")=="seller")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "products/product_confirm_delete.html", {"product": product})

# --- Cart ---
@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("buyer_dashboard")

@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    item.delete()
    return redirect("cart_detail")

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    if request.method == "POST":
        order = Order.objects.create(user=request.user, total_amount=total, is_paid=True)
        cart.items.all().delete()
        messages.success(request, f"Order {order.id} placed successfully!")
        return redirect("product_list")
    return render(request, "cart/checkout.html", {"cart": cart, "total": total})

# --- Mentorship ---
@login_required
def send_request(request, mentor_id):
    mentor = get_object_or_404(User, id=mentor_id)
    if getattr(mentor.profile, "role", "") != "mentor":
        messages.error(request, "This user is not a mentor.")
        return redirect("mentor_directory")
    
    if MentorshipRequest.objects.filter(mentor=mentor, mentee=request.user, status="Pending").exists():
        messages.warning(request, "Request already sent.")
        return redirect("mentor_directory")

    MentorshipRequest.objects.create(mentor=mentor, mentee=request.user, message="Hello!")
    messages.success(request, f"Mentorship request sent to {mentor.username}")
    return redirect("mentor_directory")

@login_required
def requests_inbox(request):
    if getattr(request.user.profile, "role", "") != "mentor":
        messages.error(request, "Only mentors can view requests.")
        return redirect("mentor_directory")
    requests_list = MentorshipRequest.objects.filter(mentor=request.user).order_by("-created_at")
    return render(request, "core/requests_inbox.html", {"requests": requests_list})

@login_required
def request_action(request, pk, action):
    req = get_object_or_404(MentorshipRequest, pk=pk, mentor=request.user)
    if action.lower() == "accept":
        req.status = "Accepted"
        messages.success(request, f"You accepted {req.mentee.username}'s request.")
    elif action.lower() == "reject":
        req.status = "Rejected"
        messages.warning(request, f"You rejected {req.mentee.username}'s request.")
    else:
        messages.error(request, "Invalid action.")
        return redirect("requests_inbox")
    req.save()
    return redirect("requests_inbox")

@login_required
def mentor_directory(request):
    mentors = User.objects.filter(profile__role="mentor")
    return render(request, "mentors/mentor_directory.html", {"mentors": mentors})

@login_required
def mentor_profile_detail(request, mentor_id):
    mentor = get_object_or_404(User, id=mentor_id, profile__role="mentor")
    profile = get_object_or_404(Profile, user=mentor)
    return render(request, "mentors/mentor_profile_detail.html", {"mentor": mentor, "profile": profile})

@login_required
def mentor_profile_edit(request):
    if getattr(request.user.profile, "role", "") != "mentor":
        messages.error(request, "No permission to edit mentor profile.")
        return redirect("home")
    
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = MentorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("mentor_directory")
    else:
        form = MentorProfileForm(instance=profile)
    return render(request, "mentors/mentor_profile_edit.html", {"form": form})

# --- Savings ---
@login_required
def savings_home(request):
    groups = SavingsGroup.objects.all()
    return render(request, "savings/savings_home.html", {"groups": groups})

@login_required
def savings_group_detail(request, group_id):
    group = get_object_or_404(SavingsGroup, id=group_id)
    return render(request, "savings/savings_group_detail.html", {"group": group})

# --- Home ---
def home(request):
    return render(request, "home.html")