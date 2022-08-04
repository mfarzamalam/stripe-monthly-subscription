from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Product

from django.contrib import messages


# Create your views here.

def home_page(request):
    return render(request, 'product/home.html')


def view_product(request):
    product_qs = Product.objects.all()
    context = {'products': product_qs}
    return render(request, 'product/view_product.html', context)


def add_product(request):
    if request.method == "POST":
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        desc = request.POST.get('product_desc')
        image = request.POST.get('product_image')
        print("name:", name)
        print("price:", price)
        print("desc:", desc)
        print("image:", image)

        product_obj = Product.objects.create(name=name, price=price, description=desc, image=image)
        messages.success(request, 'Successfully Added Product.')

        return HttpResponseRedirect("/")

    else:
        if request.method == "GET":
            return render(request, 'product/add_product.html')