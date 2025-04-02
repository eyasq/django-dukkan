from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from alnaser.models import Category, Customer, Order, Product
from django.contrib.auth.models import User
from .forms import SignUpForm,ProductAddForm
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

# Create your views here.

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    category_id = request.GET.get('category', None)
    if category_id and category_id != 'all':
        products = products.filter(category__id=category_id)
    
    categories = Category.objects.all()
    context = {
        "products":products,
        "categories":categories
    }
    request.session.categories = categories
    return render(request, 'index.html', context)


def about(request):

    return render(request, 'about.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #log in user
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "Succesfully Registered!")
            return redirect('home')
        else:
            messages.error(request, "Error registering. Please Try Again")
            return redirect('/register')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {"form":form})

def login_user(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']
        password = request.POST['password']
        if '@' in identifier:
            try:
                user = User.objects.get(email = identifier)
                username = user.username
            except User.DoesNotExist:
                messages.error(request, 'User Does Not Exist')
                return redirect('/login')
        else:
            try:
                customer = Customer.objects.get(phone = identifier)
                username = customer.user.username
            except Customer.DoesNotExist:
                messages.error(request, 'User Does Not Exist')
                return redirect('/login')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('/')
        else:
            messages.error(request, 'Invalid password. Please Try Again.')
            return redirect('/login')
    else:
        return render(request, 'login.html')
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')
    

def product_show(request, product_id):
    product = Product.objects.get(id = product_id)
    return render(request, 'product_page.html', {"product":product})

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name = foo)
        products = Product.objects.filter(category = category)
        return render(request, 'category.html', {"prdoucts":products, "category":category})
    except:
        messages.error(request, 'No Such Category')
        return redirect('/')
    
@login_required(login_url='/login')
def account(request):
    user= request.user
    customer = user.customer
    orders = customer.orders.all().order_by('-created_at')

    context = {
        "user":user,
        "customer":customer,
        "orders":orders
    }

    return render(request, 'account.html', context)

@login_required(login_url='/login')
@require_POST
def edit_account(request):
    user = request.user
    customer = user.customer
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    errors = {}
    if not username:
        errors['username'] = 'Username is required'
    elif len(username) < 5:
        errors['username'] = 'Username must be at least 5 characters'
    if not email:
        errors['email'] = 'Email is required'
    elif User.objects.exclude(pk=request.user.pk).filter(email=email).exists():
        errors['email'] = 'Email is already in use'
    customer_errors = Customer.objects.customer_validator(request.POST, current_user = user)
    errors.update(customer_errors)
    if not errors:
            # Update only changed fields
        if user.username != username:
            user.username = username
        if user.first_name != first_name:
            user.first_name = first_name
        if user.last_name != last_name:
            user.last_name = last_name
        if user.email != email:
            user.email = email
        user.save()
            
        if customer.address != address:
            customer.address = address
        if customer.phone != phone:
            customer.phone = phone
            customer.save()
            
        messages.success(request, 'Profile updated successfully!')
        return redirect('/')
    else:
        context = {
                'errors': errors,
                'original_values': request.POST
            }
        return render(request, 'account.html', context)
    
def delete_order(request, order_id):
    order = Order.objects.get(id = order_id)
    order.delete()
    messages.success(request, 'Order cancelled')
    return redirect('/')
    

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account')  # Redirect to profile page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})
def staff_check(user):
    return user.is_staff

@login_required
@user_passes_test(staff_check, login_url='/login/')
def add_product(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('home')  # Redirect to product list page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductAddForm()
    
    return render(request, 'products/add_product.html', {'form': form})