from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.db import transaction

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user if request.user.is_authenticated else None
                    
                    if user:
                        cart_items = Cart.objects.filter(user=user)
                    else:
                        # Use session_key for anonymous users
                        cart_items = Cart.objects.filter(session_key=request.session.session_key)

                    if cart_items.exists():
                        #sozdat zakaz
                        order=Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            e_mail=form.cleaned_data['e_mail'],
                        )
                        #sozdat zakazanie tovari
                        for cart_item in cart_items:
                            product=cart_item.product
                            name=cart_item.product.title
                            price=cart_item.products_price()
                            quantity=cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Insufficient quantity of goods {name}\ In stock {product.quantity}')
                            
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                                )
                            product.quantity -= quantity
                            product.save()

                        #o4istit korzinu posle zakaza
                        cart_items.delete()

                        messages.success(request, 'The order has been placed')
                        return redirect('profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('create_order')
    else:
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'phone_number': request.user.phone_number,
                'street_and_house_number': request.user.street_and_house_number,
                'additional_address': request.user.additional_address,
                'postcode': request.user.postcode,
                'location': request.user.location,
                'e_mail': request.user.email,
            }
        else:
            initial = {
                'first_name': '',
                'last_name': '',
                'phone_number': '',
                'street_and_house_number': '',
                'additional_address': '',
                'postcode': '',
                'location': '',
                'e_mail': '',
            }
    
        form = CreateOrderForm(initial=initial)

    context={
        'form':form,
    }
    return render(request, 'orders/create_order.html', context=context)


