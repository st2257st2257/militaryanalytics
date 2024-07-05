from django.contrib import admin

# Register your models here.
from orders.models import SubDivType, OrderType, Order
"""Basket"""

admin.site.register(SubDivType)
admin.site.register(OrderType)
admin.site.register(Order)
"""admin.site.register(Basket)"""
