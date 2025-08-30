from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Product, Cart, CartItem, Order

from rest_framework import generics, permissions

from .forms import (
    SignUpForm, ProductForm, SavingsGroupForm,
    MentorProfileForm, MentorshipRequestForm
)
from .models import (
    User, Product, Cart, CartItem, Order,
    BusinessTemplate, SavingsGroup, SavingsMember, Loan, MentorProfile, MentorshipRequest
)
from .serializers import (
    UserSerializer, ProductSerializer, OrderSerializer,
    BusinessTemplateSerializer, SavingsGroupSerializer, LoanSerializer,
    MentorProfileSerializer, MentorshipRequestSerializer
)

User = get_user_model()

def custom_logout(request):
    """Custom logout view that accepts both GET and POST requests"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def home(request):
   
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    
    return render(request, 'home.html')

def community(request):
    return render(request, 'core/community.html')

def opportunities(request):
    return render(request, 'core/opportunities.html')

def about(request):
    return render(request, 'core/about.html')

@login_required
def seller_dashboard(request):
    # Get products for the current user (seller)
    products = Product.objects.filter(seller=request.user)
    
    # Calculate total sales
    total_sales = 0
    try:
        total_sales = Order.objects.filter(
            items__product__seller=request.user,
            is_paid=True
        ).aggregate(total=Sum('total_amount'))['total'] or 0
    except:
        total_sales = 0
    
    # Get cart count for authenticated users
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    context = {
        'products': products,
        'total_sales': total_sales,
        'cart_items_count': cart_items_count,
    }
    
    return render(request, 'dashboards/seller_dashboard.html', context)

@login_required
def mentor_dashboard(request):
    # Get cart count for authenticated users
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    context = {
        'cart_items_count': cart_items_count,
    }
    
    return render(request, 'dashboards/mentor_dashboard.html', context)

@login_required
def mentee_dashboard(request):
    # Get cart count for authenticated users
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    context = {
        'cart_items_count': cart_items_count,
    }
    
    return render(request, 'dashboards/mentee_dashboard.html', context)


@login_required
def buyer_dashboard(request):

    featured_products = Product.objects.filter(is_featured=True)[:6]
    
   
    if not hasattr(request.user, 'id') or not request.user.is_authenticated:
        messages.error(request, "Authentication error. Please log in again.")
        return redirect('login')
    
  
    if isinstance(request.user, str):
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')
    else:
        user = request.user
    
    user_orders = Order.objects.filter(buyer=user).order_by('-created_at')[:5]
    
    products = Product.objects.filter(is_featured=True)[:6]
    
   
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items_count = cart.items.count()
    
  
    try:
        total_spent = Order.objects.filter(
            buyer=user, 
            is_paid=True
        ).aggregate(total=Sum('total_amount'))['total'] or 0
    except:
        total_spent = 0
    
    try:
        orders_count = Order.objects.filter(buyer=user).count()
    except:
        orders_count = 0
    
    context = {
        'featured_products': featured_products,
        'user_orders': user_orders,
        'cart_items_count': cart_items_count,
        'total_spent': total_spent,
        'orders_count': orders_count,
        "products": products,
        'now': timezone.now(),
    }
    
    return render(request, 'dashboards/buyer_dashboard.html', context)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


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
        serializer.save(buyer=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class BusinessTemplateListView(generics.ListAPIView):
    queryset = BusinessTemplate.objects.all()
    serializer_class = BusinessTemplateSerializer
    permission_classes = [permissions.AllowAny]


class SavingsGroupListCreateView(generics.ListCreateAPIView):
    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class SavingsGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)


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



# Authentication
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Get the selected role from the form
            role = request.POST.get('role')
            if role:
                user.role = role
                # Set the appropriate boolean fields based on role
                if role == 'seller':
                    user.is_seller = True
                elif role == 'mentor':
                    user.is_mentor = True
            
            user.save()
            login(request, user)
            
            # Redirect based on the selected role
            if role == 'buyer':
                messages.success(request, "Account created successfully! Welcome to your Buyer Dashboard!")
                return redirect("buyer_dashboard")
            elif role == 'seller':
                messages.success(request, "Account created successfully! Welcome to your Seller Dashboard!")
                return redirect("seller_dashboard")
            elif role == 'mentor':
                messages.success(request, "Account created successfully! Welcome to your Mentor Dashboard!")
                return redirect("mentor_dashboard")
            elif role == 'mentee':
                messages.success(request, "Account created successfully! Welcome to your Mentee Dashboard!")
                return redirect("mentee_dashboard")
            elif role == 'saver':
                messages.success(request, "Account created successfully! Welcome to your Savings Dashboard!")
                return redirect("savings_home")
            else:
                # Default fallback
                messages.success(request, "Account created successfully!")
                return redirect("dashboard_home")
        else:
         
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    
    return render(request, "core/auth/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in successfully!")
            return redirect("dashboard_home")  
    else:
        form = AuthenticationForm()
    return render(request, "core/auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("login")


# @login_required
# def post_login_redirect(request):
#     return redirect("home")

# --- Dashboards ---
@login_required
def dashboard_home(request):
    
    return render(request, 'dashboard_home.html')

@login_required
def dashboard(request):
   
    return redirect("dashboard_home")

# Products
def product_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        products = products.filter(category__iexact=category)
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    

    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    return render(request, "core/product_list.html", {
        "page_obj": page_obj,
        "cart_items_count": cart_items_count
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    return render(request, "core/product_detail.html", {
        "product": product,
        "cart_items_count": cart_items_count
    })


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Product created successfully!")
            return redirect("product_list")  
    else:
        form = ProductForm()
    
    # Get cart count
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.items.count()
    
    return render(request, "core/product_form.html", {
        "form": form,
        "cart_items_count": cart_items_count
    })

@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_list")  
    else:
        form = ProductForm(instance=product)
    
    # Get cart count
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.items.count()
    
    return render(request, "core/product_form.html", {
        "form": form,
        "cart_items_count": cart_items_count
    })

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("product_list")  #
    
    # Get cart count
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.items.count()
    
    return render(request, "core/product_confirm_delete.html", {
        "product": product,
        "cart_items_count": cart_items_count
    })

# --- Cart ---
@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.items.count()
    
    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
    
    return render(request, "cart/cart_detail.html", {
        "cart": cart,
        "cart_items_count": cart_items_count,
        "total_amount": total_amount
    })

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        item.quantity += 1
        item.save()
        messages.info(request, f"Added another {product.name} to your cart.")
    else:
        messages.success(request, f"Added {product.name} to your cart.")
    
    return redirect("product_list")

@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"Removed {product_name} from your cart.")
    return redirect("cart_detail")

@login_required
def update_cart_item(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, f"Updated {item.product.name} quantity.")
        else:
            item.delete()
            messages.success(request, f"Removed {item.product.name} from cart.")
    
    return redirect("cart_detail")

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_detail")
    
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    
    if request.method == "POST":
        # Create order
        order = Order.objects.create(
            buyer=request.user, 
            total_amount=total, 
            is_paid=True
        )
        
        # Add items to order
        for item in cart.items.all():
            order.items.add(item)
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect("dashboard_home")
    
    cart_items_count = cart.items.count()
    
    return render(request, "cart/checkout.html", {
        "cart": cart, 
        "total": total,
        "cart_items_count": cart_items_count
    })

# Mentorship 
@login_required
def send_request(request, mentor_id):
    messages.info(request, "Mentorship request feature coming soon!")
    return redirect("mentor_directory")

@login_required
def requests_inbox(request):
    messages.info(request, "Requests inbox feature coming soon!")
    return redirect("home")

@login_required
def request_action(request, pk, action):
    messages.info(request, "Request action feature coming soon!")
    return redirect("requests_inbox")

@login_required
def mentor_directory(request):
  
    messages.info(request, "Mentor directory feature coming soon!")
    return redirect("home")

@login_required
def mentor_profile_detail(request, mentor_id):
   
    messages.info(request, "Mentor profile feature coming soon!")
    return redirect("home")

@login_required
def mentor_profile_edit(request):
  
    messages.info(request, "Mentor profile edit feature coming soon!")
    return redirect("home")

# Savings 
@login_required
def savings_home(request):
    groups = SavingsGroup.objects.all()
    
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    return render(request, "savings/savings_home.html", {
        "groups": groups,
        "cart_items_count": cart_items_count
    })

@login_required
def savings_group_create(request):
    if request.method == 'POST':
        # Handle form submission for creating a new savings group
        messages.info(request, "Savings group creation feature coming soon!")
        return redirect("savings_home")
    
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    return render(request, "savings/savings_group_create.html", {
        "cart_items_count": cart_items_count
    })

@login_required
def savings_group_detail(request, group_id):
    group = get_object_or_404(SavingsGroup, id=group_id)
    
   
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    return render(request, "savings/savings_group_detail.html", {
        "group": group,
        "cart_items_count": cart_items_count
    })

# Orders 
@login_required
def order_history(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    # Get cart count for authenticated users
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    return render(request, "orders/order_history.html", {
        "orders": orders,
        "cart_items_count": cart_items_count
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    # Get cart count for authenticated users
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    
    return render(request, "orders/order_detail.html", {
        "order": order,
        "cart_items_count": cart_items_count
    })