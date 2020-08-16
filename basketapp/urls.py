from django.urls import path
import basketapp.views as basketapp


app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit'),
    path('remove/<int:pk>)/', basketapp.basket_remove, name='remove'),
]
