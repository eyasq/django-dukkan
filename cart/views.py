from django.shortcuts import redirect, render
from django.http import JsonResponse
import json
import math
from .cart import Cart
from alnaser.models import Product
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    context = {
        "products": cart_products
    }
    return render(request, 'cart/cart_summary.html', context)

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
