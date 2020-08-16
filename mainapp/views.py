import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import json
import random

from basketapp.models import Basket
from .models import Product, ProductCategory


def main(request):
    context = {
        'title': "Магазин",
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', context)


def contacts(request):
    context = {
        'title': "Контакты",
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contacts.html', context)


def gallery(request):
    with open(os.path.join(settings.BASE_DIR, 'static/db_goods.json'), "r", encoding="utf-8") as read_file:
        goods = json.load(read_file)
    context = {
        'title': "Галерея",
        'goods': goods,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/gallery.html', context)


def cart(request):
    context = {
        'title': "Корзина",
    }
    return render(request, 'mainapp/cart.html', context)


def categories(request):
    _categories = ProductCategory.objects.all()
    context = {
        'title': "Категории",
        'categories': _categories,
    }
    return render(request, 'mainapp/categories.html', context)


def product(request, pk=None):
    _product = get_object_or_404(Product, pk=pk)
    context = {
        'title': _product.name,
        'links_menu': ProductCategory.objects.all(),
        'product': _product,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', context)


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)

    if pk is None:
        pk = 0

    if pk == 0:
        _products = Product.objects.all().order_by('price')
        category = {'name': 'все'}
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        _products = Product.objects.filter(category__pk=pk).order_by('price')

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'products': _products,
        'basket': basket,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products_list.html', content)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    _products = Product.objects.all()
    return random.sample(list(_products), 1)[0]


def get_same_products(hot_product):
    # same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    same_products = Product.objects.exclude(pk=hot_product.pk)[:3]
    return same_products
