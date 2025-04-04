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
from django.contrib import admin
from django.urls import path

from alnaser import views

urlpatterns = [
    path('', views.index, name='home'),
    path("search/", views.search_products, name="search_products"),
    path('about', views.about, name='about'),
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('products/<int:product_id>', views.product_show),
    path('category/<str:foo>', views.category, name='category'),
    path('account', views.account, name='account'),
    path('account/edit', views.edit_account, name='edit_account'),
    path('order/delete/<int:order_id>', views.delete_order, name='delete_order'),
    path('account/change', views.change_password, name='change_password'),
    path('products/add/', views.add_product, name='add_product'),

]
