from django.urls import path
from store.views.billing_views import index, new_bill, create, receipt, generate_pdf

app_name = 'billing'

urlpatterns = [
    path('', index, name='index'),
    path('new', new_bill, name='new_bill'),
    path('create', create, name='create'),
    path('receipt/<int:id>', receipt, name='receipt'),
    path('pdf/<int:id>', generate_pdf, name='generate_pdf'),
]
