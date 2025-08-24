from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import SavingsGroup, Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import MentorProfile
from .forms import MentorProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import MentorshipRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import MentorshipRequest


@login_required
def request_action(request, req_id, action):
    """
    Approve or reject a mentorship request.
    """
    mentorship_request = get_object_or_404(MentorshipRequest, id=req_id, mentor=request.user)

    if action == "accept":
        mentorship_request.status = "Accepted"
    elif action == "reject":
        mentorship_request.status = "Rejected"

    mentorship_request.save()
    return redirect("requests_inbox")  # redirects back to the inbox page


@login_required
def requests_inbox(request):
    """
    Show all mentorship requests sent to the currently logged-in mentor.
    """
    if not request.user.is_mentor:
        return render(request, "mentors/not_a_mentor.html")

    requests = MentorshipRequest.objects.filter(mentor=request.user)
    return render(request, "mentors/requests_inbox.html", {"requests": requests})



@login_required
def mentor_profile_edit(request):
    """Allow mentors to create or edit their profile."""
    profile, created = MentorProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MentorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("mentor_profile")  # redirect to profile view
    else:
        form = MentorProfileForm(instance=profile)

    return render(request, "mentors/mentor_profile_edit.html", {"form": form})



@login_required
def savings_home(request):
    """Show all savings groups the user belongs to."""
    groups = request.user.savings_groups.all()  # from ManyToMany in SavingsGroup
    return render(request, "savings/savings_home.html", {"groups": groups})


@login_required
def savings_group_detail(request, pk):
    """Show details of a specific savings group."""
    group = get_object_or_404(SavingsGroup, pk=pk)
    transactions = Transaction.objects.filter(group=group).order_by("-date")
    return render(
        request,
        "savings/savings_group_detail.html",
        {"group": group, "transactions": transactions},
    )


def get_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# View Cart
@login_required
def cart_view(request):
    cart = get_cart(request.user)
    items = cart.cartitem_set.all()
    return render(request, "cart/cart_view.html", {"cart": cart, "items": items})


# Add Item to Cart
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart_view")


# Remove Item from Cart
@login_required
def remove_from_cart(request, pk):
    cart = get_cart(request.user)
    item = get_object_or_404(CartItem, pk=pk, cart=cart)
    item.delete()
    return redirect("cart_view")


@login_required
def checkout(request):
    cart = get_cart(request.user)
    items = cart.cartitem_set.all()

    if request.method == "POST":
        order = Order.objects.create(user=request.user, total=0)
        total = 0
        for item in items:
            total += item.product.price * item.quantity
            
        order.total = total
        order.save()

        # Clear cart
        items.delete()

        return redirect("order_detail", pk=order.pk)

    return render(request, "cart/checkout.html", {"cart": cart, "items": items})

@login_required
def dashboard(request):
    """
    Show different dashboards based on user role.
    """
    user = request.user
    context = {}

    if user.is_seller:
        # Seller dashboard: show products
        products = user.products.all()
        context["products"] = products
        return render(request, "dashboards/seller_dashboard.html", context)

    elif user.is_mentor:
        # Mentor dashboard: show requests (placeholder)
        requests = user.received_requests.all() if hasattr(user, "received_requests") else []
        context["requests"] = requests
        return render(request, "dashboards/mentor_dashboard.html", context)

    else:
        # Buyer dashboard: show cart/orders
        cart = getattr(user, "cart", None)
        orders = user.orders.all() if hasattr(user, "orders") else []
        context["cart"] = cart
        context["orders"] = orders
        return render(request, "dashboards/buyer_dashboard.html", context)


from .forms import (
    SignupForm, ProductForm,
    SavingsGroupForm, TransactionForm,
    MentorProfileForm, MentorshipRequestForm
)
from .models import (
    Product, Cart, CartItem, Order,
    SavingsGroup, SavingsMember, Transaction,
    MentorProfile, MentorshipRequest
)

from django.shortcuts import redirect

def post_login_redirect(request):
    """
    Redirect users to the right dashboard/homepage depending on their role.
    """
    user = request.user
    if user.is_authenticated:
        if user.is_seller:
            return redirect("product_list")  # seller goes to their product dashboard
        elif user.is_mentor:
            return redirect("mentorship_dashboard")  # mentors see mentorship
        else:
            return redirect("home")  # normal buyers go to homepage/shop
    return redirect("login")



def is_seller(user):
    return hasattr(user, "is_seller") and user.is_seller

def is_mentor(user):
    return hasattr(user, "is_mentor") and user.is_mentor


def product_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query))
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
@user_passes_test(is_seller)
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
@user_passes_test(is_seller)
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
@user_passes_test(is_seller)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "products/product_confirm_delete.html", {"product": product})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    item.delete()
    messages.info(request, "Item removed from cart.")
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



@login_required
def savings_dashboard(request):
    groups = request.user.savings_groups.all()
    return render(request, "savings/dashboard.html", {"groups": groups})


@login_required
def create_savings_group(request):
    if request.method == "POST":
        form = SavingsGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            SavingsMember.objects.create(user=request.user, group=group, balance=0)
            messages.success(request, "Savings group created.")
            return redirect("savings_dashboard")
    else:
        form = SavingsGroupForm()
    return render(request, "savings/create_group.html", {"form": form})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(SavingsGroup, pk=pk)
    members = SavingsMember.objects.filter(group=group)
    return render(request, "savings/group_detail.html", {"group": group, "members": members})


@login_required
def add_transaction(request, pk):
    group = get_object_or_404(SavingsGroup, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.group = group
            transaction.save()
            member, created = SavingsMember.objects.get_or_create(user=request.user, group=group)
            member.balance += transaction.amount
            member.save()
            group.total_savings += transaction.amount
            group.save()
            messages.success(request, "Transaction added.")
            return redirect("group_detail", pk=group.pk)
    else:
        form = TransactionForm()
    return render(request, "savings/add_transaction.html", {"form": form, "group": group})

@login_required
@user_passes_test(is_mentor)
def mentor_profile(request):
    profile, created = MentorProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = MentorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("mentor_profile")
    else:
        form = MentorProfileForm(instance=profile)
    return render(request, "mentorship/mentor_profile.html", {"form": form})


def mentor_directory(request):
    mentors = MentorProfile.objects.filter(availability=True)
    return render(request, "mentorship/mentor_directory.html", {"mentors": mentors})


@login_required
def send_request(request, mentor_id):
    mentor = get_object_or_404(MentorProfile, pk=mentor_id)
    if request.method == "POST":
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.mentee = request.user
            req.mentor = mentor.user
            req.save()
            messages.success(request, "Request sent.")
            return redirect("mentor_directory")
    else:
        form = MentorshipRequestForm()
    return render(request, "mentorship/send_request.html", {"form": form, "mentor": mentor})


@login_required
@user_passes_test(is_mentor)
def mentorship_requests(request):
    requests_list = MentorshipRequest.objects.filter(mentor=request.user)
    return render(request, "mentorship/requests.html", {"requests": requests_list})


@login_required
@user_passes_test(is_mentor)
def handle_request(request, pk, action):
    req = get_object_or_404(MentorshipRequest, pk=pk, mentor=request.user)
    if action == "accept":
        req.status = "Accepted"
    elif action == "reject":
        req.status = "Rejected"
    req.save()
    messages.info(request, f"Request {action}ed.")
    return redirect("mentorship_requests")


def home(request):
    return render(request, "home.html")


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


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("login")
