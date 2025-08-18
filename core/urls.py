from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.create_product, name="create_product"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/update/", views.update_product, name="update_product"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),
]