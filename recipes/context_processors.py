def shoplist(request):
    cart = request.session['cart']
    return {'cart': cart}
