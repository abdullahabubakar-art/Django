from django.urls import path
from products.views import product_create, render_initial_data, dynamic_lookup_view, product_delete_view, product_list_view

app_name = 'products'
urlpatterns = [
    path('initial/', render_initial_data),
    path('', product_list_view, name='product-list'),
    path('create/', product_create, name='product_create'),
    path('<int:id>/', dynamic_lookup_view, name='product-details'),
    path('<int:id>/delete/', product_delete_view, name='product-delete')
]
