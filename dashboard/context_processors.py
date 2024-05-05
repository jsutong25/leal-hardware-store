from .models import CartItems, Cart

def cart_count_processor(request):
    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(user=request.user).first()

        if user_cart:
            cart_count = CartItems.objects.filter(cart=user_cart).count()
        else:
            cart_count = 0
    else:
        cart_count = 0 

    return {'cart_count': cart_count}
