from django.shortcuts import render
import json


def main(request):
    context = {
        'title': "Магазин",
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request):
    with open("static/db_goods.json", "r", encoding="utf-8") as read_file:
        goods = json.load(read_file)
    context = {
        'title': "Каталог товаров",
        'goods': goods,
    }
    return render(request, 'mainapp/catalog.html', context)


def contacts(request):
    context = {
        'title': "Контакты",
    }
    return render(request, 'mainapp/contacts.html', context)


def gallery(request):
    with open("static/db_goods.json", "r", encoding="utf-8") as read_file:
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
