from django.contrib import admin

from alnaser.models import Category, Customer, Order, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
