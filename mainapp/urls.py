from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
   path('', mainapp.catalog, name='catalog'),
   path('<int:pk>/', mainapp.products, name='product'),
]
