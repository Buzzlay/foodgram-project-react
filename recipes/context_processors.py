def shoplist(request):
    cart = request.session.setdefault('cart', {})
    return {'cart': cart}
