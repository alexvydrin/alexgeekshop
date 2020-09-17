from basketapp.models import Basket


def basket(request):
    # print(f'context processor basket works')
    _basket = []

    if request.user.is_authenticated:
        _basket = Basket.objects.filter(user=request.user)
        # _basket = Basket.get_items(request.user)
        # _basket = request.user.basket.select_related() - уменьшается количество запросов

    return {
        'basket': _basket,
    }
