from django.db import models

from users.models import User

# Create your models here.


class SubDivType(models.Model):
    shortName = models.CharField(max_length=128, blank=False)
    shortText = models.CharField(max_length=128, blank=False)
    fullText = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.shortName} {self.shortText}'


class OrderType(models.Model):
    subDivType = models.ForeignKey(to=SubDivType, on_delete=models.PROTECT)
    shortName = models.CharField(max_length=128, blank=False)
    shortText = models.CharField(max_length=128, blank=False)
    fullText = models.TextField(null=True, blank=True)
    averagePrice = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='orders_images')


class Order(models.Model):
    userId = models.IntegerField(default=0)
    orderType = models.ForeignKey(to=OrderType, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    orderPrice = models.DecimalField(max_digits=6, decimal_places=2)


class BasketQuerySet(models.QuerySet):
    def totalSum(self):
        return sum(basket.sum() for basket in self)

    def totalQuantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=OrderType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.name} | Продукт'

    def sum(self):
        return self.product.averagePrice * self.quantity
