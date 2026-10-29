from django.urls import path
from store.views.suppliers_views import index, add, edit, delete

app_name = 'suppliers'

urlpatterns = [
    path('', index, name='index'),
    path('add', add, name='add'),
    path('edit/<int:id>', edit, name='edit'),
    path('delete/<int:id>', delete, name='delete'),
]
