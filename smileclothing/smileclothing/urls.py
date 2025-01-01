"""
URL configuration for smileclothing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from smileapp.views import orders_list,contact_view,buy_now,home,order_confirmation,register_view,login_view,cart_view,login_required,logout_view,profile_view,product_list,product_detail,add_to_cart,remove_from_cart,order_detail,checkout,view_orders,ProductListView,create_product
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/",register_view,name="register"),
    path('login/', login_view, name='login'),
    path('home/',home,name='home'),
    path('logout_required/',login_required,name="logout_required"),
    path('logout/',logout_view,name='logout'),
    path('products/',product_list, name='product_list'),
    path('products/<int:id>/<slug:slug>/',product_detail, name='product_detail'),
    path('products/category/<slug:category_slug>/',product_list, name='product_list_by_category'),
    path('products/<int:id>/<slug:slug>/',product_detail, name='product_detail'),
    path('orders/',view_orders, name='orders'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('order/<int:order_id>/',order_detail, name='order_detail'),
    path('checkout/', checkout, name='checkout'),
    path('create-product/', create_product, name='create-product'), 
    path('products/', ProductListView.as_view(), name='product_list'),  # No arguments
    path('products/<slug:slug>/', ProductListView.as_view(), name='product_list_by_category'),  # With slug for categories
    path('products/<int:id>/<slug:slug>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/<slug:slug>/',add_to_cart, name='add_to_cart'),
    path('cart/',cart_view, name='cart_view'),
    path('profile/',profile_view, name='profile'),
    path('contact/', contact_view, name='contact_view'),  # Define your contact URL
    path('contact/', contact_view, name='contact'),  # Ensure this line exists
    path('add_to_cart/<int:id>/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('buy_now/<int:id>/<slug:slug>/',buy_now, name='buy_now'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('orders/', orders_list, name='orders_list'),

   




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



