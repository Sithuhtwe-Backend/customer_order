"""accounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from importlib import import_module
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard, name="dashboard"),
    path('customers/<str:id>', views.customers, name="customers.show"),
    path('products/',views.products, name="products"),
    path('orders/create/<int:customerId>', views.orderCreate, name="order.create"),
    path('orders/update/<int:orderId>', views.orderUpdate, name="order.update"),
    path('orders/delete/<int:orderId>', views.orderDelete, name="order.delete"),
    path('register', views.register, name="register"),
    path('login', views.userLogin, name="login"),
    path('logout', views.userLogout, name="logout"),
    path('customer_profile', views.customer_profile, name="customer_profile"),
    path('customer_profile_setting', views.customer_profile_setting, name="customer_profile_setting"),
    
    
]
