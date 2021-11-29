from app.models import Orders
from app.models import SubOrders

def cart(request):
    if request.user.is_authenticated:
        currentOrder = Orders.objects.filter(holder=request.user, status='incart').first()
        if currentOrder == None:
            cart_items = 0
        else:
            cart_items = SubOrders.objects.filter(order=currentOrder).count()
    else:
        cart_items = 0
    return {'cart_items': cart_items}