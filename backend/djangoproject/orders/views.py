from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
import os
import subprocess
from subprocess import check_output

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from orders.models import OrderType, Order, Basket

from users.models import User

from users.views import \
    addIp, ip_save


@ip_save
@csrf_exempt
def index_order(request):
    if request.method == 'POST':
        pass
    orderType = OrderType.objects.all()
    arrContext = []
    for order in orderType:
        context = {"sale": "x1.5",
                   "price1": str(order.averagePrice),
                   "price2": str(order.averagePrice),
                   "title": order.shortName,
                   "id": order.id,
                   "url": 'imgs' + str(order.image.url)[6:]}
        print('imgs' + str(order.image.url)[6:])
        arrContext.append(context)
    return render(request, 'order/index.html',
                  context={"name": arrContext})


@ip_save
@login_required
def basket_add(request, product_id):
    product = OrderType.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@ip_save
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@ip_save
@login_required
def send_money(request, number):
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
