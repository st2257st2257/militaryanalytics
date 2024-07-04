# @Aleksandr Kristal v0.0.1 || create all
from products.models import \
    Product, \
    Commodity, \
    Service, \
    DroneHub, \
    SellerOrder
from typing import Dict
from app1.config import \
    dictStatus
from app1.services import \
    send_email
from users.models import \
    User
from datetime import datetime
import re
from datetime import datetime


def _get_seller_login(productId: int) -> str:
    """Возвращает логин продавца по ID или сигнализирует об его отсутствии"""
    if len(Product.objects.filter(id=productId)) == 1:
        return Product.objects.get(id=productId).userLogin
    else:
        return "Not defined"


def _add_product(data) -> Dict[str, any]:
    """Добавляет продукт по словарю из запроса"""
    product = Product(
        userLogin=data.get('userLogin', 'test_user'),
        name=data.get('name', 'test_product_name'),
        price=data.get('price', 'test_product_price'),
        description=data.get('description', 'test_product_description'),
        type=data.get('type', 'test_product_type'),
        characteristics=data.get('characteristicsID', 'test_product_characteristics'))
    product.save()
    return {"result": True,
            "productName": product.name,
            "price": product.price}


def _get_characteristics_list(product_object: Product):
    """Возвращения списка характеристик продукта в зависимости от типа продукта"""
    characteristics_list = {}
    if product_object.type == "commodity":
        characteristics_list = \
            Commodity.objects.get(id=product_object.characteristicsID).getAllDicts()
    elif product_object.type == "service":
        characteristics_list = \
            Service.objects.get(id=product_object.characteristicsID).getAllDicts()
    elif product_object.type == "droneHub":
        characteristics_list = \
            DroneHub.objects.get(id=product_object.characteristicsID).getAllDicts()
    else:
        # Error with chars
        pass
    return characteristics_list


def _make_result(productObject: Product, characteristics_list) -> Dict[str, any]:
    """Формирует правильный словарь для вывода на фронт"""
    return {"result": True,
            "userLogin": productObject.userLogin,
            "companyName": _get_company_name(productObject.userLogin),
            "name": productObject.name,
            "price": productObject.price,
            "description": productObject.description,
            "type": productObject.type,
            "ggz": productObject.ggz,
            "appends": characteristics_list}


def _get_product(product_id: int, productName: str) -> Dict[str, any]:
    """Возвращает продукт в виде словаря по ID и его Name"""
    if len(Product.objects.filter(id=product_id)) == 1:
        product_object = Product.objects.get(id=product_id)
        product_object.save()
        characteristics_list = _get_characteristics_list(product_object)
        return _make_result(product_object, characteristics_list)
    elif len(Product.objects.filter(name=productName)) == 1:
        product_object = Product.objects.get(name=productName)
        product_object.save()
        characteristics_list = _get_characteristics_list(product_object)
        return _make_result(product_object, characteristics_list)
    else:
        return {"result": dictStatus.get(211)}


def _get_all_product() -> Dict[any, any]:
    """Получение всех продуктов"""
    result = {"result": True}
    for product in Product.objects.all():
        characteristicsList = _get_characteristics_list(product)
        result[product.id] = {"userLogin": product.userLogin,
                              "companyName": _get_company_name(product.userLogin),
                              "name": product.name,
                              "price": product.price,
                              "description": product.description,
                              "type": product.type,
                              "ggz": product.ggz,
                              "appends": characteristicsList}
    return result


def _get_company_name(login: str) -> str:
    if len(User.objects.filter(login=login)) == 1:
        user = User.objects.get(login=login)
        company_name = user.companyName
        return company_name
    else:
        "Название компании"



def _get_company_email(login: str) -> str:
    if len(User.objects.filter(login=login)) == 1:
        user = User.objects.get(login=login)
        company_email = user.login
        return company_email
    else:
        "email@naletay.shop"


def _get_company_phone(login: str) -> str:
    if len(User.objects.filter(login=login)) == 1:
        user = User.objects.get(login=login)
        company_phone = user.phone
        return company_phone
    else:
        "+7-999-888-77-66"


def _get_company_full_name(login: str) -> str:
    if len(User.objects.filter(login=login)) == 1:
        user = User.objects.get(login=login)
        firstNM = user.firstNM
        secondNM = user.secondNM
        thirdNM = user.thirdNM
        return firstNM + " " + \
               secondNM + " " + \
               thirdNM
    else:
        "ФИО"


def get_dict_characteristic(product):
    chat_dict = {}
    if product.type == "service":
        service = Service.objects.get(id=product.characteristicsID)
        chat_dict["category"] = service.category
        chat_dict["subCategory"] = service.subCategory
        chat_dict["productName"] = service.productName
        chat_dict["specifications"] = ''
    else:
        commodity = Commodity.objects.get(id=product.characteristicsID)
        chat_dict["category"] = commodity.category
        chat_dict["subCategory"] = commodity.subCategory
        chat_dict["productName"] = commodity.productName
        chat_dict["specifications"] = get_specifications(commodity)
    return chat_dict


def get_specifications(commodity):
    specifications = {}
    # print(self.specification,self.specification.split("\\"),len(self.specification.split("\\")))
    if len(commodity.specification.split("\\")) == len(commodity.specification.split("|")):
        for item in commodity.specification.split("\\"):
            # print(item,item.split("\\"),len(item.split("\\")))
            if len(item.split("|")) == 2:
                specifications.update({clear_str(item.split("|")[0]): item.split("|")[1]})
    return specifications


def _get_order_res(order, product, characteristic) -> Dict[any, any]:
    """Формирует словарь для отправки данных заказа на фронт"""
    orderRes = {"user_login": order.userLogin,
                "user_name": _get_company_name(order.userLogin),
                "user_full_name": _get_company_full_name(order.userLogin),
                "user_phone": _get_company_phone(order.userLogin),
                "product_id": order.productID,
                "category": characteristic["category"],
                "subCategory": characteristic["subCategory"],
                "productName": characteristic["productName"],
                "specifications": characteristic["specifications"],
                "totalPrice": product.price * order.quantity,
                "date": order.date,
                "chat_id": order.chatID,
                "quantity": order.quantity,
                "seller_login": order.sellerLogin,
                "seller_name": _get_company_name(order.sellerLogin),
                "seller_email": _get_company_email(order.sellerLogin),
                "seller_phone": _get_company_phone(order.sellerLogin),
                "seller_full_name": _get_company_full_name(order.sellerLogin),
                "order_status_id": order.orderStatusId}
    return orderRes


def get_pre_order_dict():
    return {
        "total_sum": 0,
        "seller_login": "",
        "seller_name": "",
        "seller_phone": "",
        "user_login": "",
        "user_role": "",
        "user_full_name": "",
        "user_phone": "",
        "user_email": "",
        "user_company_name": ""
    }


def create_final_result(result, order, seller_order, user_role):
    """Заполняет JSON для выдачи на сервер"""
    product = Product.objects.get(id=order.productID)
    characteristic = get_dict_characteristic(product)
    orderRes = _get_order_res(order, product, characteristic)
    order_final_dict = {
        "orderId": order.id,
        "orderRes": orderRes
    }
    if order.sellerLogin not in result.keys():
        result[order.sellerLogin] = {}
    if seller_order.id not in result[order.sellerLogin].keys():
        result[order.sellerLogin][seller_order.id] = get_pre_order_dict()

    result[order.sellerLogin][seller_order.id][order.id] = order_final_dict
    result[order.sellerLogin][seller_order.id]["total_sum"] += \
        order_final_dict["orderRes"]["totalPrice"]
    result[order.sellerLogin][seller_order.id]["seller_login"] = \
        order_final_dict["orderRes"]["seller_login"]
    result[order.sellerLogin][seller_order.id]["seller_name"] = \
        order_final_dict["orderRes"]["seller_name"]
    result[order.sellerLogin][seller_order.id]["seller_phone"] = \
        order_final_dict["orderRes"]["seller_phone"]
    result[order.sellerLogin][seller_order.id]["user_login"] = \
        order_final_dict["orderRes"]["user_login"]
    result[order.sellerLogin][seller_order.id]["user_full_name"] = \
        order_final_dict["orderRes"]["user_full_name"]
    result[order.sellerLogin][seller_order.id]["user_email"] = \
        order_final_dict["orderRes"]["user_login"]
    result[order.sellerLogin][seller_order.id]["user_phone"] = \
        order_final_dict["orderRes"]["user_phone"]
    result[order.sellerLogin][seller_order.id]["user_company_name"] = \
        order_final_dict["orderRes"]["user_name"]
    result[order.sellerLogin][seller_order.id]["user_role"] = user_role
    return result


def _get_dict_orders_by_user_seller_login(user_login: str, seller_login: str):
    """Возвращает список заказов в формате словаря по логину и продавцу"""
    result = {}
    for seller_order in SellerOrder.objects.filter(userLogin=user_login,
                                                   sellerLogin=seller_login):
        user_role = "buyer"
        order_id_list = [int(item) for item in seller_order.orderIdList.split(',')]
        for order_id in order_id_list:
            order = Order.objects.get(id=order_id)
            result = create_final_result(result, order, seller_order, user_role)
    return result


def _get_dict_orders_by_user_login(user_login: str):
    """Возвращает список заказов в формате словаря по логину"""
    result = {}
    for seller_order in SellerOrder.objects.filter(userLogin=user_login):
        user_role = "buyer"
        order_id_list = [int(item) for item in seller_order.orderIdList.split(',')]
        for order_id in order_id_list:
            order = Order.objects.get(id=order_id)
            result = create_final_result(result, order, seller_order, user_role)

    for seller_order in SellerOrder.objects.filter(sellerLogin=user_login):
        user_role = "seller"
        order_id_list = [int(item) for item in seller_order.orderIdList.split(',')]
        for order_id in order_id_list:
            order = Order.objects.get(id=order_id)
            result = create_final_result(result, order, seller_order, user_role)
    return result


def _get_all_user_orders(token: str) -> Dict[any, any]:
    """Возвращает все заказы пользователя по токену"""
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        result = _get_dict_orders_by_user_login(user.login)
        return {"result": True,
                "data": result}
    else:
        return {"result": dictStatus.get(111)}


def _get_all_user_orders_by_seller(token: str, seller: str) -> Dict[any, any]:
    """Возвращает все заказы пользователя по токену и названию продавца"""
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        result = _get_dict_orders_by_user_seller_login(user.login, seller)
        return {"result": True,
                "data": result}
    else:
        return {"result": dictStatus.get(111)}


def _get_all_user_orders_by_seller_order_id(
        token: str,
        seller_order_id: int) -> Dict[any, any]:
    """Возвращает все заказы пользователя по токену и названию продавца"""
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        result = {}
        seller = ""
        sellerOrderIdList = []
        if len(SellerOrder.objects.filter(id=seller_order_id)) == 1:
            sellerOrder = SellerOrder.objects.get(id=seller_order_id)
            seller = sellerOrder.sellerLogin
            sellerOrderIdList = sellerOrder.orderIdList.split(',')
        for order in Order.objects.filter(
                userLogin=user.login,
                sellerLogin=seller):
            if str(order.id) in sellerOrderIdList:
                product = Product.objects.get(id=order.productID)
                characteristic = get_dict_characteristic(product)
                orderRes = _get_order_res(order, product, characteristic)
                order_final_dict = {
                    "orderId": order.id,
                    "orderRes": orderRes
                }
                if order.sellerLogin not in result.keys():
                    result[order.sellerLogin] = {}
                    result[order.sellerLogin][order.id] = order_final_dict
                else:
                    result[order.sellerLogin][order.id] = order_final_dict
        for order in Order.objects.filter(
                sellerLogin=user.login):
            if str(order.id) in sellerOrderIdList:
                product = Product.objects.get(id=order.productID)
                characteristic = get_dict_characteristic(product)
                orderRes = _get_order_res(order, product, characteristic)
                order_final_dict = {
                    "orderId": order.id,
                    "orderRes": orderRes
                }
                if order.sellerLogin not in result.keys():
                    result[order.sellerLogin] = {}
                    result[order.sellerLogin][order.id] = order_final_dict
                else:
                    result[order.sellerLogin][order.id] = order_final_dict
        return {"result": True,
                "data": result}
    else:
        return {"result": dictStatus.get(111)}


def clear_str(string):
    new_str = re.sub(" ","",string)
    return re.sub("\n","",new_str)


def _create_one_order(
        token: str,
        productId: int,
        quantity: int,
        chat_id: int) -> Dict[any, any]:
    """Создание одного заказа"""
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        order = Order(
               userLogin=user.login,
               productID=productId,
               date=datetime.now(),
               chatID=chat_id,
               quantity=quantity,
               sellerLogin=_get_seller_login(productId))
        order.save()
        return {"result": True,
                "orderId": order.id}
    else:
        return {"result": dictStatus.get(111)}


def _create_multi_order(
        token: str,
        product_id_array: str,
        quantity_array: str) -> Dict[any, any]:
    """Создание нескольких заказов"""
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        # проходимся по списку заказов и добавляем для каждого продавца заказы
        orders = {}
        new_orders_id_list = []
        for i in range(len(product_id_array.split(','))):
            product_id = product_id_array.split(',')[i]
            quantity = quantity_array.split(',')[i]
            product = Product.objects.get(id=product_id)
            if product.userLogin not in orders.keys():
                orders[product.userLogin] = {}
            orders[product.userLogin][product_id] = {}
            orders[product.userLogin][product_id]['productId'] = int(product_id)
            orders[product.userLogin][product_id]['quantity'] = int(quantity)
            # Создание заказа относящегося к одному продукту
            new_orders_id_list.append(
                _create_one_order(
                    token,
                    product_id,
                    quantity,
                    -1).get('orderId', -1))
            orders[product.userLogin][product_id]['orderId'] = int(new_orders_id_list[-1])

        for seller_order in orders.keys():
            product_id_list = ""
            order_quantity_list = ""
            new_orders_list = ""
            for key in orders[seller_order].keys():
                order_quantity_list += str(orders[seller_order][str(key)]['quantity']) + ","
                product_id_list += str(orders[seller_order][str(key)]['productId']) + ","
                new_orders_list += str(orders[seller_order][str(key)]['orderId']) + ","
            seller_order = SellerOrder(userLogin=user.login,
                                       sellerLogin=seller_order,
                                       orderIdList=new_orders_list[:-1],
                                       productIdList=product_id_list[:-1],
                                       orderQuantityList=order_quantity_list[:-1])
            seller_order.save()
        return {"result": True}
    else:
        return {"result": dictStatus.get(111)}



def _edit_order_status(token: str, orderId: int, newStatus: int):
    """Редактирование статуса заказа"""
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        if len(Order.objects.filter(id=orderId)) == 1:
            if len(Order.objects.filter(userLogin=user.login,
                                        id=orderId)) == 1:
                order = Order.objects.get(id=orderId)
                order.orderStatusId = newStatus
                order.save()
            elif user.accessID > 3:
                order = Order.objects.get(id=orderId)
                order.orderStatusId = newStatus
                order.save()
            elif len(Order.objects.filter(sellerLogin=user.login,
                                          id=orderId)) == 1:
                order = Order.objects.get(id=orderId)
                order.orderStatusId = newStatus
                order.save()
            else:
                return {"result": dictStatus.get(112)}
        else:
            return {"result": dictStatus.get(211)}
        return {"result": True}
    else:
        return {"result": dictStatus.get(111)}


def send_email_leasing(token: str,
                       full_name: str,
                       email: str,
                       company_name: str,
                       phone: str,
                       message: str,
                       product_id: int,
                       quantity: int):
    if len(User.objects.filter(token=token)) == 1:
        user = User.objects.get(token=token)
        title = f"Была оформлена заявка на лизин. Id {user.id}"
        text = f"Заявка в лизинг на товар {product_id} в количестве {quantity}\n\n"\
               f"Покупатель:\n"\
               f"\tНазвание компании: {company_name}\n" \
               f"\tТелефон: {phone}\n" \
               f"\tИмя покупателя: {full_name}\n" \
               f"\tСообщение: {message}\n\n" \
               f"Вы заказали этот товар в {str(datetime.now())[:19]}"
        send_email(title,
                   text,
                   "kristal.as@phystech.edu")
        # send_email(title, text, email)
        return {"result": True}
    else:
        return {"result": dictStatus.get(111)}
