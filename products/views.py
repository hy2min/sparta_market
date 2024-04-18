from django.shortcuts import get_object_or_404, render,redirect

from products.forms import ProductForm
from products.models import Product
from django.views.decorators.http import require_POST, require_http_methods


def list(request) :
    products = Product.objects.all()
    context = {"products" : products}
    return render(request,"products/list.html",context)

def detail(request, product_id) :
    product = get_object_or_404(Product, pk = product_id)
    return render(request, "products/detail.html", {'product' : product})

def create(request) :
    form = ProductForm()
    if request.method == "POST" :
        form = ProductForm(request.POST)
        if form.is_valid() :
            form.save()
        return redirect("products:list")
    context = {'form':form}
    return render(request,"products/create.html",context)

def update(request, product_id) :
    product = get_object_or_404(Product, pk = product_id)
    if request.method == 'POST' :
        form = ProductForm(request.POST, instance= product)
        if form.is_valid() :
            form.save()
            return redirect("products:detail",product.id)
    else :
        form = ProductForm(instance = product)
    context = {
        'form':form,
        'product' : product
        }
    return render(request,"products/update.html", context)

@require_POST
def delete(request,product_id) :
    product = get_object_or_404(Product, pk = product_id)
    product.delete()
    return redirect("products:list")
