from .cart import Cart

#create context processor so cart can work accross all site pages

def cart(request):
    #return default data form Cart
    return {"cart":Cart(request)}