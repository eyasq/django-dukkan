from alnaser.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get existing cart from session or create a new one
        cart = self.session.get('cart', {})
        
        # Ensure cart exists in session
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id in self.cart:
            # Product already in cart
            return False

        # Add new product to cart
        self.cart[product_id] = {
            'price': float(product.price),
            'quantity': int(quantity),
            'total_price': float(product.price) * int(quantity)
        }

        self.session.modified = True
        return True
    
    def __len__(self):
        # Calculate total quantity of items in cart
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        # Attach quantity and total price to products
        for product in products:
            cart_item = self.cart.get(str(product.id), {})
            product.cart_quantity = cart_item.get('quantity', 1)
            product.cart_total_price = cart_item.get('total_price', product.price)
        
        return products
    
    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            # Ensure quantity is an integer
            quantity = int(quantity)
            
            # Update quantity and recalculate total price
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['total_price'] = self.cart[product_id]['price'] * quantity
            
            self.session.modified = True
            return True
        return False
    def remove(self, product_id):
   
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
            return True
        return False