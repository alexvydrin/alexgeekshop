import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import json

from basketapp.models import Basket
from .models import Product, ProductCategory


def main(request):
    context = {
        'title': "Магазин",
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request):
    # ТОDO: не функция используется в проекте - удалить
    _products = Product.objects.all()
    context = {
        'title': "Каталог товаров",
        'products': _products,
    }
    return render(request, 'mainapp/catalog.html', context)


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
        'product': _product,
    }
    return render(request, 'mainapp/product.html', context)


def products(request, pk=None):

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    if pk is None:
        pk = 0

    if pk == 0:
        _products = Product.objects.all().order_by('price')
        category = {'name': 'все'}
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        _products = Product.objects.filter(category__pk=pk).order_by('price')

    content = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'products': _products,
        'basket': basket,
    }

    return render(request, 'mainapp/products_list.html', content)
