from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard:index')),
    path('auth/', include('store.urls_auth', namespace='auth')),
    path('dashboard/', include('store.urls_dashboard', namespace='dashboard')),
    path('inventory/', include('store.urls_inventory', namespace='inventory')),
    path('billing/', include('store.urls_billing', namespace='billing')),
    path('suppliers/', include('store.urls_suppliers', namespace='suppliers')),
]

handler404 = 'store.views.dashboard_views.custom_404_view'
