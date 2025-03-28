

from alnaser.models import Product


class Cart():
    def __init__(self, request):

        self.session = request.session

        #get session key if exist
        cart = self.session.get('session_key')
        
        #if user = new, no session key, create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available all accross site
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            return False
        self.cart[product_id] = {'price':str(product.price)}     
        self.session.modified =  True
        return True
    def __len__(self):
        return len(self.cart)  
    
    def get_products(self):
        product_ids = self.cart.keys() #list of product id's in cart
        products = Product.objects.filter(id__in = product_ids)

        return products