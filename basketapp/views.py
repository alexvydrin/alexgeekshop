from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    _basket = Basket.objects.filter(user=request.user, product=product).first()
    if not _basket:
        _basket = Basket(user=request.user, product=product)
    _basket.quantity += 1
    _basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    content = {pk: pk}
    return render(request, 'basketapp/basket.html', content)
