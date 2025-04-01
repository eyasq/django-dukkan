from django.shortcuts import redirect, render
from django.http import JsonResponse
import json
import math
from .cart import Cart
from alnaser.models import Order, OrderItem, Product
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    context = {
        "products": cart_products
    }
    return render(request, 'cart/cart_summary.html', context)
@login_required(login_url='/login')
def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            product = Product.objects.get(id=product_id)
            
            # Try to add product
            added = cart.add(product=product, quantity=quantity)
            
            if not added:
                # Product already in cart
                return JsonResponse({
                    'success': False, 
                    'message': 'Product is already in the cart'
                }, status=400)
            
            cart_quantity = cart.__len__()
            return JsonResponse({'qty': cart_quantity, 'success': True})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

@require_POST
@csrf_protect
@login_required(login_url='/login')
def update_cart(request):
    cart = Cart(request)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)
        
        # Verify product exists
        Product.objects.get(id=product_id)
        
        updated = cart.update_quantity(product_id, quantity)
        
        if updated:
            return JsonResponse({
                'success': True, 
                'qty': cart.__len__(),
                'total_price': cart.cart[str(product_id)]['total_price']
            })
        else:
            return JsonResponse({
                'success': False, 
                'error': 'Product not found in cart'
            }, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

@login_required(login_url='/login')
def cart_remove(request, product_id):

    cart = Cart(request)
    
    try:
        # Convert product_id to the correct type if needed
        product_id = int(product_id)
        
        # Remove the product from the cart
        removed = cart.remove(product_id)
        
        if removed:
            # Redirect back to cart summary with a success message
            return redirect('cart_summary')
        else:
            # Product not found in cart
            return redirect('cart_summary')
    
    except (ValueError, TypeError):
        # Invalid product ID
        return redirect('cart_summary')
    
@login_required(login_url='/login')
def check_out_page(request):
    cart = Cart(request)
    # Get products in the cart
    cart_products = cart.get_products()
    # Calculate total cart value
    total_cart_value = sum(
        product.cart_total_price for product in cart_products
    )
    # Get total number of items
    total_items = len(cart)
    
    context = {
        'products': cart_products,
        'total_cart_value': math.ceil(total_cart_value),
        'total_items': total_items,
        'current_user': request.user
    }
    return render(request, 'cart/check_out_page.html', context)

@login_required(login_url='/login')
def make_order(request):
    # to make an order, the order model requires:
    # customer, who is the currently logged in user, status will be pending upon creation, total price is the the total_cart_value, shipping address is a manual input.
    # post form gives: extra address, extra contact number, notes
    # use the rest of data in request to populate the other fields.
    cart = Cart(request)
    # Get products in the cart
    cart_products = cart.get_products()
    # Calculate total cart value
    total_cart_value = sum(
        product.cart_total_price for product in cart_products
    )
    # Get total number of items
    total_items = len(cart)
    
    context = {
        'products': cart_products,
        'total_cart_value': math.ceil(total_cart_value),
        'total_items': total_items,
        'current_user': request.user
    }
    # after creating, an order model, i need to create an order item instance for each item
    #make an order manager and use it to validate the order details.
    post_data = request.POST
    errors = Order.objects.order_validator(post_data)
    if errors:
        request.session['errors'] = errors
        messages.error(request, 'Order Failed!')
        return redirect('/cart/checkout')
    
    new_order = Order.objects.create(
        customer = request.user.customer,
        status = 'pending',
        total_price = math.ceil(total_cart_value),
        shipping_address = post_data.get('address_extra'),
        info = post_data.get('notes'),
        contact = post_data.get('contact_extra'),
    )
    for product in cart_products:
        OrderItem.objects.create(
            order = new_order,
            product = product,
            quantity = product.cart_quantity,
            price = product.price
        )
    request.session['cart'] = {}

    messages.success(request, 'Order placed Successfully!')
    return redirect('/')

    
