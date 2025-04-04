"""
URL configuration for soloproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from cart import views
from django.contrib import admin
from django.urls import path





urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('checkout', views.check_out_page, name='checkout'),
    path('make_order', views.make_order, name='make_order')
]
