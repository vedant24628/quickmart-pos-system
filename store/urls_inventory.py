from django.urls import path
from store.views.inventory_views import index, add, edit, delete, api_products

app_name = 'inventory'

urlpatterns = [
    path('', index, name='index'),
    path('add', add, name='add'),
    path('edit/<int:id>', edit, name='edit'),
    path('delete/<int:id>', delete, name='delete'),
    path('api/products', api_products, name='api_products'),
]
