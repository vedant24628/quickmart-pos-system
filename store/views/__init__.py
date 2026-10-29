# Views package
from store.views.auth_views import login_view, register_view, logout_view, login_required
from store.views.dashboard_views import index as dashboard_index, api_revenue, api_category_sales, api_top_products, custom_404_view
from store.views.inventory_views import index as inventory_index, add as inventory_add, edit as inventory_edit, delete as inventory_delete, api_products
from store.views.billing_views import index as billing_index, new_bill, create as billing_create, receipt as billing_receipt, generate_pdf
from store.views.suppliers_views import index as suppliers_index, add as suppliers_add, edit as suppliers_edit, delete as suppliers_delete

__all__ = [
    'login_view', 'register_view', 'logout_view', 'login_required',
    'dashboard_index', 'api_revenue', 'api_category_sales', 'api_top_products', 'custom_404_view',
    'inventory_index', 'inventory_add', 'inventory_edit', 'inventory_delete', 'api_products',
    'billing_index', 'new_bill', 'billing_create', 'billing_receipt', 'generate_pdf',
    'suppliers_index', 'suppliers_add', 'suppliers_edit', 'suppliers_delete',
]
