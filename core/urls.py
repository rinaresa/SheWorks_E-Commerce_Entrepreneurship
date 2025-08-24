from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
path('', views.home, name='home'),
path("redirect/", views.post_login_redirect, name="post_login_redirect"),



path('login/', auth_views.LoginView.as_view(template_name='core/auth/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('signup/', views.signup_view, name='signup'),

path('post-login-redirect/', views.post_login_redirect, name='post_login_redirect'),


path('dashboard/', views.dashboard, name='dashboard'),

path("products/", views.product_list, name="product_list"),
path("products/<int:pk>/", views.product_detail, name="product_detail"),
path("products/create/", views.create_product, name="create_product"),
path("products/<int:pk>/update/", views.update_product, name="update_product"),
path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),

path("cart/", views.cart_view, name="cart_view"),
path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
path("cart/checkout/", views.checkout, name="checkout"),


path('savings/', views.savings_home, name='savings_home'),
path('savings/<int:group_id>/', views.savings_group_detail, name='savings_group_detail'),

path('mentors/', views.mentor_directory, name='mentor_directory'),
path('mentors/profile/', views.mentor_profile_edit, name='mentor_profile_edit'),
path("mentors/profile/edit/", views.mentor_profile_edit, name="mentor_profile_edit"),  
path('mentors/<int:mentor_id>/request/', views.send_request, name='send_request'),
path('mentors/requests/', views.requests_inbox, name='requests_inbox'),
path('mentors/requests/<int:req_id>/action/<str:action>/', views.request_action, name='request_action'),
]