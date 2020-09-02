"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
# from django.contrib import admin
from django.urls import path, re_path
from mainapp import views

urlpatterns = [
    re_path('^$', views.main, name="main"),
    path('', include('social_django.urls', namespace='social')),
    path('contacts/', views.contacts, name="contacts"),
    path('gallery/', views.gallery, name="gallery"),
    path('cart/', views.cart, name="cart"),
    path('product/<int:pk>/', views.product, name="product"),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    re_path(r'^order/', include('ordersapp.urls', namespace='order')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    # path('catalog/', views.catalog, name="catalog"),
    # path('categories/', views.categories, name="categories"),
    # path('product/0/', views.products, name="catalog"),
    # path('admin_old/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
