from django.urls import path
from store.views.dashboard_views import index, api_revenue, api_category_sales, api_top_products

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),
    path('api/revenue/<str:timeframe>', api_revenue, name='api_revenue'),
    path('api/category/sales', api_category_sales, name='api_category_sales'),
    path('api/top/products', api_top_products, name='api_top_products'),
]
