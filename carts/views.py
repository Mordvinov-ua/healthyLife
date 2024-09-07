from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from carts.models import Cart
from carts.utils import get_user_carts
from herbs.models import Tovar, TovarVariation

from django.shortcuts import get_object_or_404

def cart_add(request):
    product_id = request.POST.get("product_id")
    variation_id = request.POST.get("variation_id")

    print(f"Received product_id: {product_id}, variation_id: {variation_id}")

    product = get_object_or_404(Tovar, id=product_id)
    variation = get_object_or_404(TovarVariation, id=variation_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product, variation=variation)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, variation=variation, quantity=1)
    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product, variation=variation)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key, product=product, variation=variation, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Product added to basket",
        "cart_items_html": cart_items_html,
    }

    # Возвращаем JsonResponse с данными
    return JsonResponse(response_data)
    

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": cart}, request=request
    )

    response_data = {
        "message":"Quantity changed",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity
    }

    return JsonResponse(response_data)

def cart_remove(request):
    cart_id = request.POST.get("cart_id")
    print(f"cart_id: {cart_id}")
    cart = Cart.objects.get(id=cart_id)
    print(f"cart: {cart}")
    cart.delete()
    

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message":"Product delete",
        "cart_items_html": cart_items_html,
    }
    
    return JsonResponse(response_data)

def tovar_detail(request, tovar_slug):
    # Получаем объект товара по его slug
    tovar = get_object_or_404(Tovar, slug=tovar_slug)
    
    # Здесь можно установить ID вариации вручную или получить его из запроса, если это необходимо
    # Пример получения вариации из запроса
    variation_id = request.GET.get('variation_id')
    
    # Получаем цену товара с учётом вариации
    price = tovar.get_price(variation_id=variation_id)
    
    # Передаём товар и цену в шаблон
    context = {
        'tovar': tovar,
        'price': price,
    }
    
    return render(request, 'included_cart.html', context)
