from django.shortcuts import get_object_or_404, render,redirect

from products.forms import ProductForm
from products.models import Product
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

def list(request) :
    products = Product.objects.all()
    context = {"products" : products}
    return render(request,"products/list.html",context)

def detail(request, product_id) :
    product = get_object_or_404(Product, pk = product_id)
    return render(request, "products/detail.html", {'product' : product})

@login_required
def create(request) :
    form = ProductForm()
    if request.method == "POST" :
        form = ProductForm(request.POST)
        if form.is_valid() :
            product = form.save()
        return redirect("products:list", product.id)
    else :
        form = ProductForm()
    context = {'form':form}
    return render(request,"products/create.html",context)

@login_required
@require_http_methods(["GET","POST"])
def update(request, product_id) :
    product = get_object_or_404(Product, pk = product_id)
    if request.method == 'POST' :
        form = ProductForm(request.POST, instance= product)
        if form.is_valid() :
            product = form.save()
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
    if request.user.is_authenticated :
        product = get_object_or_404(Product, pk = product_id)
        product.delete()
    return redirect("products:list")
