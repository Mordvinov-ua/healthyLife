from django.shortcuts import render

from herbs.utils import q_search
from .models import *
from django.core.paginator import Paginator


def mainPage(request):
    contact_list = Sale_tovar.objects.all()
    paginator = Paginator(contact_list, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mainPage.html', {'page_obj':page_obj, 'value':3})

def sale_cat(request, sale_cat_id):
    contact_list = Sale_tovar.objects.all()
    paginator = Paginator(contact_list, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mainPage.html', {'page_obj':page_obj, 'value':sale_cat_id})

def showCat (request, cat_slug):
    return render (request, 'groupPage.html', {'slug':cat_slug})

def priceList (request, priceList_slug):

    order_by = request.GET.get('order_by', None)

    contact_list = Tovar.objects.all()
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

    paginator = Paginator(contact_list, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render (request, 'search.html', {'page_obj':page_obj,},)

def tovar (request, tovar_slug,):
    return render (request, 'tovar.html', {'slug':tovar_slug})

