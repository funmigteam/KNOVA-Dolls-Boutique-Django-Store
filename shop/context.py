from .models import Cart, StoreSettings
def cart_context(request):
    count=0; cart=None
    try:
        cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else Cart.objects.filter(session_key=request.session.session_key).first()
        count=sum(i.quantity for i in cart.items.all()) if cart else 0
    except Exception: pass
    return {'cart_count':count,'current_cart':cart,'store_settings':StoreSettings.objects.first()}
