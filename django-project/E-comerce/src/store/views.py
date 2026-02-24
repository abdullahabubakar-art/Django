from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.forms.models import model_to_dict 
from django.views  import View
from .models import Product
import json

@xframe_options_exempt
def checkout_iframe(request):
    return render(request, "checkout_iframe.html")

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def get(self, req):
        queryset = list(Product.objects.values())

        return JsonResponse(queryset, safe=False)
    
    def post(self, req, *args, **Kwargs):
        data = json.loads(req.body)
        queryset = Product.objects.create(
            name = data.get('name'),
            price = data.get('price'),
            description = data.get('description'),  
            image = data.get('image')
        )
        
        res = model_to_dict(queryset)
        
        # FIX: Replace the ImageField object with its URL string
        # This prevents the "Object of type ImageFieldFile is not JSON serializable" error
        if queryset.image:
            res = str(queryset.image.url) 
        else:
            res = ""

        return JsonResponse(res, safe=False)

    

@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailView(View):
    def get(self, req, id):
        queryset = Product.objects.filter(id=id).values().first()
        res ={
            'product': queryset
        }
        return JsonResponse(queryset)

    
    def put(self, req, id):
        data = json.loads(req.body)

        queryset = Product.objects.filter(id=id)
        queryset.update(**data)

        res = {
            'message': f"Product {id} updated successfully!"
        }
        return JsonResponse(res)
    
    def delete(self, req, id):
        Product.objects.filter(id = id).delete()

        res = {
            'message': 'Product deleted'
        }
        return JsonResponse(res)