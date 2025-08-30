from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    UserListView,
    ProductListCreateView, ProductDetailView,
    OrderListCreateView, OrderDetailView,
    BusinessTemplateListView,
    SavingsGroupListCreateView, SavingsGroupDetailView,
    LoanListCreateView,
    MentorProfileListCreateView, MentorProfileDetailView,
    MentorshipRequestListCreateView,
)

urlpatterns = [
    # Home
    path("", views.home, name="home"),
    path('community/', views.community, name='community'),
    path('opportunities/', views.opportunities, name='opportunities'),
    path('about/', views.about, name='about'),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="core/auth/login.html"), name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("signup/", views.signup_view, name="signup"),

     # Dashboard Homepage
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    
    # Dashboard Tabs
    path("dashboard/buyer/", views.buyer_dashboard, name="buyer_dashboard"),
    path("dashboard/seller/", views.seller_dashboard, name="seller_dashboard"),
    path("dashboard/mentor/", views.mentor_dashboard, name="mentor_dashboard"),
    path("dashboard/mentee/", views.mentee_dashboard, name="mentee_dashboard"),
    path("savings/", views.savings_home, name="savings_home"),
    

    # Products
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/create/", views.create_product, name="create_product"),
    path("products/<int:pk>/update/", views.update_product, name="update_product"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),
    path("api/products/", ProductListCreateView.as_view(), name="product-list"),

    # Cart
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:pk>/", views.update_cart_item, name="update_cart_item"),
    path("cart/checkout/", views.checkout, name="checkout"),
    
    # Orders
    path("orders/", views.order_history, name="order_history"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),

    # Savings
    path("savings/", views.savings_home, name="savings_home"),
    path("savings/create/", views.savings_group_create, name="savings_group_create"),
    path("savings/<int:group_id>/", views.savings_group_detail, name="savings_group_detail"),

    # Mentorship
    path("mentors/", views.mentor_directory, name="mentor_directory"),
    path("mentors/profile/edit/", views.mentor_profile_edit, name="mentor_profile_edit"),
    path("mentors/<int:mentor_id>/request/", views.send_request, name="send_request"),
    path("mentors/requests/", views.requests_inbox, name="requests_inbox"),
    path("mentors/requests/<int:req_id>/action/<str:action>/", views.request_action, name="request_action"),
    path("mentors/edit/", views.mentor_profile_edit, name="mentor_profile_edit"),
    path("mentors/<int:mentor_id>/", views.mentor_profile_detail, name="mentor_profile_detail"),

    # API Endpoints
    path("api/users/", UserListView.as_view(), name="user-list"),
    path("api/products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("api/orders/", OrderListCreateView.as_view(), name="order-list"),
    path("api/orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("api/business-templates/", BusinessTemplateListView.as_view(), name="business-template-list"),
    path("api/savings-groups/", SavingsGroupListCreateView.as_view(), name="savings-group-list"),
    path("api/savings-groups/<int:pk>/", SavingsGroupDetailView.as_view(), name="savings-group-detail"),
    path("api/loans/", LoanListCreateView.as_view(), name="loan-list"),
    path("api/mentors/", MentorProfileListCreateView.as_view(), name="mentor-list"),
    path("api/mentors/<int:pk>/", MentorProfileDetailView.as_view(), name="mentor-detail"),
    path("api/mentorship-requests/", MentorshipRequestListCreateView.as_view(), name="mentorship-request-list"),
]