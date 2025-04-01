from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from alnaser.models import Category, Customer, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

def index(request):
    products = Product.objects.all()
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
    context = {
        "user":user,
        "customer":customer
    }

    return render(request, 'account.html', context)

@login_required(login_url='/login')
@require_POST
def edit_account(request):
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

    return render(request, 'account.html', context)