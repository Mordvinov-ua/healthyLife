from django.shortcuts import get_object_or_404, render

from herbs.utils import q_search
from .models import *
from django.core.paginator import Paginator



def mainPage(request):
    # Получаем выбранную категорию из GET-параметра или используем категорию с pk=3 по умолчанию
    category_id = request.GET.get('category', 3)
    
    try:
        selected_category = Sale_category.objects.get(pk=category_id)
    except Sale_category.DoesNotExist:
        selected_category = Sale_category.objects.get(pk=3)
    
    # Фильтруем товары по выбранной категории
    contact_list = Tovar.objects.filter(sale_category=selected_category)
    # Получаем товары с первой вариацией со скидкой
    discount_items = []
    for item in contact_list:
        first_discount_variation = item.tovar_variations.filter(discount__gt=0).first()  # Находим первую вариацию со скидкой
        if first_discount_variation:
            original_price = first_discount_variation.price
            discount_percentage = first_discount_variation.discount
            price_after_discount = original_price - (original_price * discount_percentage / 100)
            discount_items.append({
                'item': item,
                'discount_variation': first_discount_variation,
                'price_after_discount': price_after_discount,
            })
            item.variation_id = first_discount_variation.id
        else:
            item.variation_id = item.tovar_variations.first().id
    # Пагинация - по 4 товару на страницу
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передаем категорию и список товаров в шаблон
    return render(request, 'mainPage.html', {
        'page_obj': page_obj,
        'discount_items':discount_items,
        'value': selected_category.pk,  # Передаем ID выбранной категории
        'sale_cat': Sale_category.objects.all()  # Передаем все категории
    })

def sale_cat(request, sale_cat_id):
    # Получаем категорию распродажи по ID
    sale_category = get_object_or_404(Sale_category, id=sale_cat_id)

    # Получаем список товаров по указанной категории распродажи
    contact_list = Tovar.objects.filter(sale_category=sale_category)

    for product in contact_list:
        if product.discount:
            product.price_after_discount = product.price * (1 - product.discount / 100)
        else:
            product.price_after_discount = product.price

    paginator = Paginator(contact_list, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mainPage.html', {'page_obj':page_obj, 'value':sale_cat_id, 'price_after_discount': product.price_after_discount})

def showCat (request, cat_slug):
    contact_list = Tovar.objects.all()

    paginator = Paginator(contact_list, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render (request, 'groupPage.html', {'slug':cat_slug, 'page_obj':page_obj,})

def priceList (request, priceList_slug):

    group = get_object_or_404(Group, slug=priceList_slug)

    order_by = request.GET.get('order_by', None)

    contact_list = Tovar.objects.filter(group=group)

    if order_by:
        contact_list = contact_list.order_by(order_by)

    paginator = Paginator(contact_list, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render (request, 'tovarList.html', {'slug':priceList_slug, 'page_obj':page_obj,}, )

def search(request,):
    
    query = request.GET.get('q', None)
    order_by = request.GET.get('order_by', None)

    contact_list = Tovar.objects.all()
    if query:
        contact_list = q_search(query)
    if order_by:
        contact_list = contact_list.order_by(order_by)

    # Добавляем данные о скидочных вариациях
    discount_items = []
    for item in contact_list:
        first_discount_variation = item.tovar_variations.filter(discount__gt=0).first()
        if first_discount_variation:
            original_price = first_discount_variation.price
            discount_percentage = first_discount_variation.discount
            price_after_discount = original_price - (original_price * discount_percentage / 100)
            discount_items.append({
                'item': item,
                'discount_variation': first_discount_variation,
                'price_after_discount': price_after_discount,
            })
            # Добавляем ID вариации со скидкой
            item.variation_id = first_discount_variation.id
        else:
            # Если скидки нет, используем первую вариацию
            item.variation_id = item.tovar_variations.first.id

    paginator = Paginator(contact_list, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render (request, 'search.html', {'page_obj':page_obj,},)


def tovar  (request, tovar_slug,):
    tovar = get_object_or_404(Tovar, slug=tovar_slug)
    variations = tovar.tovar_variations.all()

    # Создание словаря с информацией 
    variations_with_discount = [
        {      
            'id': variation.id,
            'size': variation.size,
            'price': variation.price,
            'discount': variation.discount,
            'price_after_discount': variation.price_after_discount(),
        }
        for variation in variations
    ]

    context = {
        'tovar': tovar,
        'variations_with_discount': variations_with_discount,
        'slug':tovar_slug,
    }
    
    return render  (request, 'tovar.html', context)

