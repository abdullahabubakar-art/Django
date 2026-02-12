from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import Productform, PureProductForm

# Create your views here.


def product_list_view(request):
    queryset = Product.objects.all()  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, 'products/product_list.html', context)


def product_delete_view(request, id):
    obj = get_object_or_404(Product, id=id)
    #  confirm before Delete on POST request
    if request.method == 'POST':
        obj.delete()
        return redirect('../../')

    # this will delete on GET request but we want for POST request
    # obj.delete()
    context = {
        'object': obj
    }
    return render(request, 'products/product_delete.html', context)


# dynamic lookup from url
def dynamic_lookup_view(request, id):
    # obj = Product.objects.get(id=id)

    # Handling 404 error
    # obj = get_object_or_404(Product, id=id)
    try:
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404

    context = {
        'object': obj
    }
    return render(request, 'products/product_details.html', context)


# render data in form field
def render_initial_data(request):
    initial_data = {
        'title': "this is my titile field"
    }
    obj = Product.objects.get(id=1)
    my_form = Productform(request.POST or None, instance=obj)
    if my_form.is_valid():
        my_form.save()

    context = {
        'form': my_form
    }
    return render(request, "products/product_create.html", context)


# Pure django form
# def product_create(request):
#     # this create the instance of class PureProductForm for GET method
#     my_form = PurePoductForm()
#     if request.method == "POST":
#         # (request.POST) this will pass that request, POST data as i initilize form. so we have to put in condition
#         my_form = PurePoductForm(request.POST)
#         if my_form.is_valid():
#             print(my_form.cleaned_data)
#             Product.objects.create(**my_form.cleaned_data)
#         else:
#             print(my_form.errors)

#     context = {
#         'form': my_form
#     }
#     return render(request, "products/product_create.html", context)


# Raw HTML Form
# def product_create(request):
#     print(request.GET)
#     print(request.POST)
#     if request.method == "POST":
#         my_titke = request.POST.get('title')
#         print(my_titke)
#         # Product.objects.create(title = my_titke)
#     context = {}
#     return render(request, "products/product_create.html", context)


# Django Model form
def product_create(request):
    my_form = Productform(request.POST or None)
    if my_form.is_valid():
        my_form.save()
        # rerender to clear field but actually create new instance of form
        my_form = Productform()
    context = {
        'form': my_form
    }

    return render(request, "products/product_create.html", context)


# Render Data from the Database with a Model
def product_detail_view(request, id):
    obj = Product.objects.get(id=id)
    # context = {
    #     'title': obj.title,
    #     'description': obj.description
    # }

    context = {
        'object': obj
    }

    return render(request, "products/product_details.html", context)
