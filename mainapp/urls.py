from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
   path('category/0/', mainapp.products, name='index'),
   path('category/<int:pk>/', mainapp.products, name='category'),
   path('category/<int:pk>/<int:page>/', mainapp.products, name='page'),
   path('product/<int:pk>/', mainapp.product, name='product'),
]

path('', mainapp.products, name='index'),
# path('category/<int:pk>/page/<int:page>/', mainapp.products, name='page'),
# path('page/<int:page>/', mainapp.products, name='page'),
# path('<int:pk>/', mainapp.products, name='product'),
# path('0/', mainapp.products, name="catalog"),
