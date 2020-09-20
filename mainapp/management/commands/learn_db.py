from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.models import F, When, Case, DecimalField, IntegerField
from datetime import timedelta

from ordersapp.models import OrderItem


# from mainapp.models import Product  # ProductCategory
# from django.db import connection
# from adminapp.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(Q(category__name='Серия Орион') | Q(category__name='Прочие Изделия'))

        # print(len(test_products))
        # print(test_products)

        # db_profile_by_type('learn db', '', connection.queries)

        # SELECT "mainapp_product"."id", "mainapp_product"."category_id", "mainapp_product"."name",
        #   "mainapp_product"."image", "mainapp_product"."image_small", "mainapp_product"."short_desc",
        #   "mainapp_product"."description", "mainapp_product"."price",
        #   "mainapp_product"."quantity", "mainapp_product"."is_active"
        # FROM "mainapp_product" INNER JOIN "mainapp_productcategory"
        #   ON ("mainapp_product"."category_id" = "mainapp_productcategory"."id")
        # WHERE ("mainapp_productcategory"."name"='Серия Орион' OR "mainapp_productcategory"."name"='Прочие Изделия')

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
            Q(order__updated__lte=F('order__created') + action_2__time_delta)
        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition, then=F('product__price') * F('quantity') * action_1__discount)
        action_2__price = When(action_2__condition, then=F('product__price') * F('quantity') * -action_2__discount)
        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orderss = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orderss:
            s = f'{orderitem.action_order:2} : заказ № {orderitem.pk:3} : '
            s += f'{orderitem.product.name:15} : скидка {abs(orderitem.total_price):6.2f} руб.'
            s += f'| {orderitem.order.updated - orderitem.order.created}'
            print(s)
