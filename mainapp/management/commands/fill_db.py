import json
import os
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser


def load_from_json(file_name):
    with open(os.path.join('mainapp/json', file_name + '.json'), 'r', encoding="utf-8") as infile:
        return json.load(infile)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()  # можем сделать одной строчкой с create

        products = load_from_json('products')

        Product.objects.all().delete()

        for product in products:
            category_name = product["category"]
            # Ищем категорию
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # Суперпользователь
        ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=30)
