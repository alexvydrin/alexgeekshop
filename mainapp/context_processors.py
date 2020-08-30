from basketapp.models import Basket


def basket(request):
    # print(f'context processor basket works')
    _basket = []

    if request.user.is_authenticated:
        _basket = Basket.objects.filter(user=request.user)

    return {
        'basket': _basket,
    }
