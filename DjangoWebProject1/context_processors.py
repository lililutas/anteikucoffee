from app.models import Orders
from app.models import SubOrders
from app.models import Roles

def cart(request):
    if request.user.is_authenticated:
        currentOrder = Orders.objects.filter(holder=request.user, status='incart').first()
        currentRole, status = Roles.objects.get_or_create(user = request.user)
        if status:
            currentRole.role = 'client'
            currentRole.save()
            role = 'client'
        else:
            role = currentRole.role
        if currentOrder == None:
            cart_items = 0
        else:
            cart_items = SubOrders.objects.filter(order=currentOrder).count()
    else:
        cart_items = 0
        role = None
    return {
            'cart_items': cart_items,
            'role': role
            }