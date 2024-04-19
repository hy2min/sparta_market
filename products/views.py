from itertools import product
from django.shortcuts import get_object_or_404, render,redirect

from products.forms import CommentForm, ProductForm
from products.models import Product,Comment
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

def list(request) :
    products = Product.objects.all()
    context = {"products" : products}
    return render(request,"products/list.html",context)

def detail(request, product_id) :
    product = get_object_or_404(Product, pk = product_id)
    comment_form = CommentForm()
    comments = product.comments.all()
    context = {
        "product":product,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, "products/detail.html", context)

@login_required
def create(request) :
    form = ProductForm()
    if request.method == "POST" :
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid() :
            product = form.save(commit = False)
            product.author = request.user
            product.save()
            return redirect("products:detail", product.id)
    else :
        form = ProductForm()
    context = {'form':form}
    return render(request,"products/create.html",context)

@login_required
@require_http_methods(["GET","POST"])
def update(request, product_id) :
    product = get_object_or_404(Product, pk = product_id)
    if product.author != request.user :
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
    product = get_object_or_404(Product, pk = product_id)
    if request.user.is_authenticated :
        if product.author == request.user :
            product = get_object_or_404(Product, pk = product_id)
            product.delete()
    return redirect("products:list")

@require_POST
def comment_create(request,product_id) :
    product = get_object_or_404(Product,pk = product_id)
    form = CommentForm(request.POST)
    if form.is_valid() :
        comment = form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
        return redirect("products:detail",product_id)
    
@require_POST
def comment_delete(request,product_id,comment_pk) :
    comment = get_object_or_404(Comment, pk = comment_pk)
    if comment.user == request.user :
        comment.delete()
    return redirect("products:detail", product_id)