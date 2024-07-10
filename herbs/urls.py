from django.urls import path
from herbs.views import *
from healthyLife import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', mainPage, name='home'),
    path('search/', search, name='search'),
    path('<int:sale_cat_id>/', sale_cat, name='sale_cat'),
    path('group/<slug:cat_slug>/', showCat, name='group'),
    path('pricelist/<slug:priceList_slug>/', priceList, name='priceList'),
    path('tovar/<slug:tovar_slug>/', tovar, name='tovar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)