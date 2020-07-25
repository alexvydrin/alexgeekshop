from django.shortcuts import render

def main(request):
    return render(request, 'mainapp/index.html', {})

def catalog(request):
    return render(request, 'mainapp/catalog.html', {})

def contacts(request):
    return render(request, 'mainapp/contacts.html', {})

def gallery(request):
    return render(request, 'mainapp/gallery.html', {})

def cart(request):
    return render(request, 'mainapp/cart.html', {})
