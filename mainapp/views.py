import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import json
from .models import Product, ProductCategory


def main(request):
    context = {
        'title': "Магазин",
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request):
    products = Product.objects.all()
    context = {
        'title': "Каталог товаров",
        'products': products,
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
    categories = ProductCategory.objects.all()
    context = {
        'title': "Категории",
        'categories': categories,
    }
    return render(request, 'mainapp/categories.html', context)


def products(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': product.name,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)
