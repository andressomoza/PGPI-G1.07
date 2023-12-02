from .models import Eleccion

class Carrito():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart
    
    def add(self, eleccion):
        eleccion_id = str(eleccion.id)
        precio  = eleccion.get_precio_total()
        self.cart[eleccion_id] = {'quantity': 1, 'price': precio}
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, eleccion):
        eleccion_id = str(eleccion.id)
        if eleccion_id in self.cart:
            del self.cart[eleccion_id]
            self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(item['price'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()