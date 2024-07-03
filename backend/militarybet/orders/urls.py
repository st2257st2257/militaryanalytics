from django.urls import path

from orders.views import index_order, basket_add, basket_remove, send_money

app_name = 'orders'

urlpatterns = [
    path('', index_order, name='index'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('baskets/send_money/<int:number>/', send_money, name='send_money'),
]
