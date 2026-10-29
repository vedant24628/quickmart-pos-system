from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from store.models import Product, Supplier
from store.views.auth_views import login_required

CATEGORIES = [
    'Vegetables',
    'Fruits',
    'Grocery',
    'Electronics',
    'Toiletries',
    'Decor',
    'Kitchen'
]

@login_required
def index(request):
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    status_filter = request.GET.get('status', '').strip()
    sort_by = request.GET.get('sort', 'name')
    sort_order = request.GET.get('order', 'asc')

    query = Product.objects.select_related('supplier')

    if search_query:
        query = query.filter(name__icontains=search_query)

    if category_filter and category_filter in CATEGORIES:
        query = query.filter(category=category_filter)

    products = list(query)

    # Status filtering
    if status_filter == 'critical':
        products = [p for p in products if p.stock_quantity < 10]
    elif status_filter == 'low':
        products = [p for p in products if 10 <= p.stock_quantity <= 30]
    elif status_filter == 'good':
        products = [p for p in products if p.stock_quantity > 30]

    # Sorting
    reverse = (sort_order == 'desc')
    if sort_by == 'price':
        products.sort(key=lambda p: p.price, reverse=reverse)
    elif sort_by == 'stock':
        products.sort(key=lambda p: p.stock_quantity, reverse=reverse)
    elif sort_by == 'category':
        products.sort(key=lambda p: p.category.lower(), reverse=reverse)
    else:
        products.sort(key=lambda p: p.name.lower(), reverse=reverse)

    suppliers = Supplier.objects.order_by('name')

    context = {
        'products': products,
        'categories': CATEGORIES,
        'suppliers': suppliers,
        'selected_category': category_filter,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }

    return render(request, 'inventory/index.html', context)

@login_required
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        price_raw = request.POST.get('price', '').strip()
        stock_raw = request.POST.get('stock_quantity', '').strip()
        supplier_id_raw = request.POST.get('supplier_id', '').strip()

        if not name or not category or not price_raw or not stock_raw:
            messages.error(request, 'Please fill in all mandatory product fields.')
            return redirect('inventory:index')

        try:
            price = float(price_raw)
            stock_quantity = int(stock_raw)
            if price < 0 or stock_quantity < 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Price and stock quantity must be valid non-negative numbers.')
            return redirect('inventory:index')

        supplier_id = int(supplier_id_raw) if supplier_id_raw and supplier_id_raw.isdigit() else None
        supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None

        product = Product(
            name=name,
            category=category,
            price=price,
            stock_quantity=stock_quantity,
            supplier=supplier
        )
        product.save()

        messages.success(request, f'Product "{name}" added successfully to inventory.')
        return redirect('inventory:index')

    return redirect('inventory:index')

@login_required
def edit(request, id):
    product = get_object_or_404(Product, id=id)
    suppliers = Supplier.objects.order_by('name')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        price_raw = request.POST.get('price', '').strip()
        stock_raw = request.POST.get('stock_quantity', '').strip()
        supplier_id_raw = request.POST.get('supplier_id', '').strip()

        if not name or not category or not price_raw or not stock_raw:
            messages.error(request, 'All product fields are required.')
            return render(request, 'inventory/edit.html', {'product': product, 'categories': CATEGORIES, 'suppliers': suppliers})

        try:
            price = float(price_raw)
            stock_quantity = int(stock_raw)
            if price < 0 or stock_quantity < 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Price and stock quantity must be valid non-negative numbers.')
            return render(request, 'inventory/edit.html', {'product': product, 'categories': CATEGORIES, 'suppliers': suppliers})

        supplier_id = int(supplier_id_raw) if supplier_id_raw and supplier_id_raw.isdigit() else None
        supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None

        product.name = name
        product.category = category
        product.price = price
        product.stock_quantity = stock_quantity
        product.supplier = supplier
        product.save()

        messages.success(request, f'Product "{name}" updated successfully.')
        return redirect('inventory:index')

    return render(request, 'inventory/edit.html', {'product': product, 'categories': CATEGORIES, 'suppliers': suppliers})

@login_required
def delete(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        name = product.name
        product.delete()
        messages.info(request, f'Product "{name}" has been deleted.')
    return redirect('inventory:index')

@login_required
def api_products(request):
    """Returns JSON of all in-stock products (or all products) for the billing screen"""
    products = Product.objects.select_related('supplier').order_by('name')
    return JsonResponse([p.to_dict() for p in products], safe=False)
