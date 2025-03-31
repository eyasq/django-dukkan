from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from alnaser.models import Category, Customer, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
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
    pass