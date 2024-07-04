from django.contrib import admin

# Register your models here.
from orders.models import SubDivType, OrderType, Order

admin.site.register(SubDivType)
admin.site.register(OrderType)
admin.site.register(Order)
