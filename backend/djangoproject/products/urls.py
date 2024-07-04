from django.urls import path

from products.views import \
    index_product, \
    index_get, \
    index_set

app_name = 'products'

urlpatterns = [
    path('products/', index_product),
    path('get/', index_get),
    path('set/', index_set),
]
