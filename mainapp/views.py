import os
import json
import random
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Product, ProductCategory


def main(request):
    context = {
        'title': "Магазин",
    }
    return render(request, 'mainapp/index.html', context)


@cache_page(3600)
def contacts(request):
    context = {
        'title': "Контакты",
    }
    return render(request, 'mainapp/contacts.html', context)


def gallery(request):
    with open(os.path.join(settings.BASE_DIR, 'static/db_goods.json'), "r", encoding="utf-8") as read_file:
        goods = json.load(read_file)
    context = {
        'title': "Галерея",
        'goods': goods,
    }
    return render(request, 'mainapp/gallery.html', context)


def cart(request):
    context = {
        'title': "Корзина",
    }
    return render(request, 'mainapp/cart.html', context)


def categories(request):
    _categories = get_links_menu()
    context = {
        'title': "Категории",
        'categories': _categories,
    }
    return render(request, 'mainapp/categories.html', context)


def product(request, pk=None):
    _product = get_product(pk)
    context = {
        'title': _product.name,
        'links_menu': get_links_menu(),
        'product': _product,
    }
    return render(request, 'mainapp/product.html', context)


def products(request, pk=None, page=1):

    title = 'продукты'
    links_menu = get_links_menu()

    if (pk is None) or (pk == ""):
        pk = 0

    if pk == 0:
        _products = get_products_ordered_by_price()
        category = {
            'pk': 0,
            'name': 'все',
        }
    else:
        category = get_category(pk)
        _products = get_products_in_category_ordered_by_price(pk)

    paginator = Paginator(_products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'products': products_paginator,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products_list.html', content)


def get_hot_product():
    # _products = Product.objects.filter(is_active=True, category__is_active=True)
    _products = get_products()
    # TODO: Подумать как исправить ошибку если база данных пустая
    return random.sample(list(_products), 1)[0]


def get_same_products(hot_product):
    # same_products = Product.objects.filter(is_active=True, category__is_active=True).exclude(pk=hot_product.pk)[:3]
    same_products = get_products()[:3]
    # Оптимизация sql-запросов
    # same_products = Product.objects.filter(is_active=True, category__is_active=True).exclude(pk=hot_product.pk).
    #   select_related()[:3]
    return same_products


"""
def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name+'.json'), 'r', errors='ignore') as infile:
        return json.load(infile)
"""


# Реализация низкоуровневого кеширования (memcached)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


# noinspection DuplicatedCode
def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


# noinspection DuplicatedCode
def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        _product = cache.get(key)
        if _product is None:
            _product = get_object_or_404(Product, pk=pk)
            cache.set(key, _product)
        return _product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, _products)
            return _products
        else:
            return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).\
                order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
