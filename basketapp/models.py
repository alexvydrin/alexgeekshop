from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    # кеширование
    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        # версия без применения кеширования
        # _items = Basket.objects.filter(user=self.user)
        # _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        # return _totalquantity

        # версия с применением кеширования
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        # версия без применения кеширования
        # _items = Basket.objects.filter(user=self.user)
        # _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        # return _totalcost

        # версия с применением кеширования
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)

    @classmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]

        return basket_items_dic
