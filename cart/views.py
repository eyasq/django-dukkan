import json
from django.shortcuts import render,get_object_or_404
from .cart import Cart
from alnaser.models import Product
from django.http import JsonResponse
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    context = {
        "products":cart_products
    }
    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            product = Product.objects.get(id = product_id)
            added = cart.add(product = product)
            if not added:
                return JsonResponse({'message': 'Product already in cart'}, status=400)

            #quantity:
            cart_quantity = cart.__len__()
            return JsonResponse({'qty':cart_quantity})
        except json.JSONDecodeError:
            return JsonResponse({"error":"Invalid JSON"}, status=400 )
        except Product.DoesNotExist:
            return JsonResponse({"error":"Product not found"}, status=404)






    # if request.POST.get('action') == 'post':
    #     product_id = int(request.POST.get('product_id'))
    #     product = get_object_or_404(Product, id = product_id )
    #     cart.add(product = product)

    #     response = JsonResponse({'Product Name: ': product.name})
    #     return response
    


def cart_delete(request):

    pass


def cart_update(request):


    pass