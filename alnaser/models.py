from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
import cloudinary
from cloudinary.models import CloudinaryField
# Create your models here.
def get_default_customer():
    return Customer.objects.get(user__username='eyas')


class CustomerManager(models.Manager):
    def customer_validator(self, post_data, current_user=None):
        errors = {}
        phone = post_data.get('phone')
        address = post_data.get('address')
        
        # Validate phone - exclude current user's phone if provided
        if not phone:
            errors['phone'] = 'Phone number is required'
        elif len(phone) < 10:
            errors['phone'] = 'Phone must be at least 10 digits'
        else:
            # Create queryset that excludes current user
            queryset = self.exclude(user=current_user)
            if queryset.filter(phone=phone).exists():
                errors['phone'] = 'This phone number is already registered'
        
        # Validate address
        if not address:
            errors['address'] = 'Address is required'
        elif len(address) < 10:
            errors['address'] = 'Address is too short (min 10 chars)'
            
        return errors


class OrderManager(models.Manager):
    def order_validator(self, post_data):
        errors = {}
        address = post_data.get('address_extra')
        if not address:
            errors['address'] = 'Address cannot be empty'
        if len(address) < 15: 
            errors['address'] = 'Address too short, please be more detailed.'
        contact = post_data.get('contact_extra')
        if not contact or len(contact) < 10:
            errors['contact'] = 'You must provide a valid contact number (minimum 10 chars)'
        return errors

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField( blank=True)
    image = CloudinaryField('image',folder='DjangoDukkan/', null=True, blank=True)
    category = models.ForeignKey('Category',related_name='products', on_delete=models.CASCADE )
    on_sale = models.BooleanField(default = False)
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    barcode = models.CharField(max_length=13)
    def __str__(self):
        return self.name    


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    objects = CustomerManager()
    def __str__(self):
        return self.user.username

class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey('Customer', related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=ORDER_STATUS, default='pending', max_length=50)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    shipping_address = models.TextField()
    info = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()
    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits = 5, decimal_places=2)
    def __str__(self):
        return self
    