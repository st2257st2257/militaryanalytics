# @Aleksandr Kristal v0.0.1 || add
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from products.models import \
    Product, \
    Order, \
    Basket, \
    Commodity, \
    Service, \
    DroneHub

from users.models import \
    User, \
    Chat, \
    Message, \
    getToken

from app1.services import \
    send_email

from app1.config import \
    dictStatus

from products.services import \
    _get_seller_login, \
    _add_product, \
    _get_product, \
    _get_all_product, \
    _get_all_user_orders, \
    _create_one_order, \
    _edit_order_status, \
    _create_multi_order, \
    _get_all_user_orders_by_seller, \
    _get_all_user_orders_by_seller_order_id, \
    send_email_leasing


@csrf_exempt
def index_product(request):
    """Обработчик страницы получения продуктов, обрабатывает: get, add, all"""
    if request.method == 'POST':
        request_type = request.POST['type']
        if request_type == "add":
            product_data = _add_product(request.POST)
            return JsonResponse(product_data)
        elif request_type == "get":
            product_id = -1
            product_name = request.POST['name']
            if request.POST['productId'] != "":
                product_id = int(request.POST['productId'])
            return JsonResponse(_get_product(product_id, product_name))
        elif request_type == "all":
            return JsonResponse(_get_all_product())
    return render(request, 'product/index.html')


@csrf_exempt
def index_get(request):
    """Получение заказов по токену и спецификациям"""
    if request.method == 'POST':
        action = request.POST['action']
        if action == "getAllOrders":
            token = request.POST['token']
            return JsonResponse(_get_all_user_orders(token))
        elif action == "getAllOrdersBySeller":
            token = request.POST['token']
            seller = request.POST['seller']
            return JsonResponse(_get_all_user_orders_by_seller(token, seller))
        elif action == "getAllOrdersBySellerOrderId":
            token = request.POST['token']
            sellerOrderId = request.POST['sellerOrderId']
            return JsonResponse(
                _get_all_user_orders_by_seller_order_id(
                    token,
                    sellerOrderId))
    return render(request, 'product/index_get.html')


@csrf_exempt
def index_set(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == "setOne":
            token = request.POST['token']
            product_id = request.POST.get('productId', 1)
            quantity = request.POST.get('quantity', 1)
            chat_id = request.POST.get('chatID', 1)
            leasing = int(request.POST.get('leasing', -1))
            if leasing == 1:
                full_name = request.POST.get('fullName', '')
                email = request.POST.get('email', '')
                company_name = request.POST.get('companyName', '')
                phone = request.POST.get('phone', '')
                message = request.POST.get('message', '')
                send_email_leasing(token,
                                   full_name,
                                   email,
                                   company_name,
                                   phone,
                                   message,
                                   product_id,
                                   quantity)
            return JsonResponse(_create_one_order(token, product_id, quantity, chat_id))
        elif action == "editStatus":
            token = request.POST.get('token', '_')
            orderId = request.POST.get('orderId', 0)
            newStatus = request.POST.get('newStatus', 0)
            return JsonResponse(_edit_order_status(token, orderId, newStatus))
        elif action == "setMulti":
            token = request.POST.get('token', '_')
            product_id_array = request.POST.get('productIdArray', '_')
            quantity_array = request.POST.get('quantityArray', '_')
            return JsonResponse(_create_multi_order(token, product_id_array, quantity_array))
    return render(request, 'product/index_set.html')
