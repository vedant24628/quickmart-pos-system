from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, F
from django.utils import timezone
from store.models import Bill, BillItem, Product
from store.views.auth_views import login_required

CATEGORIES = [
    'Vegetables', 'Fruits', 'Grocery', 'Electronics',
    'Toiletries', 'Decor', 'Kitchen'
]

@login_required
def index(request):
    now = timezone.now()
    today_start = datetime(now.year, now.month, now.day)
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)

    # 1. Today's Revenue
    today_revenue = Bill.objects.filter(timestamp__gte=today_start).aggregate(
        total=Sum('total_amount')
    )['total'] or 0.0

    # 2. Weekly Revenue (Last 7 days)
    weekly_revenue = Bill.objects.filter(timestamp__gte=seven_days_ago).aggregate(
        total=Sum('total_amount')
    )['total'] or 0.0

    # 3. Monthly Revenue (Last 30 days)
    monthly_revenue = Bill.objects.filter(timestamp__gte=thirty_days_ago).aggregate(
        total=Sum('total_amount')
    )['total'] or 0.0

    # 4. Total Bills Count
    total_bills = Bill.objects.count()

    # 5. Total Products Count
    total_products = Product.objects.count()

    # 6. Critical Stock Count (stock < 10)
    critical_stock_count = Product.objects.filter(stock_quantity__lt=10).count()
    low_stock_count = Product.objects.filter(stock_quantity__gte=10, stock_quantity__lte=30).count()
    good_stock_count = Product.objects.filter(stock_quantity__gt=30).count()

    # Recent bills
    recent_bills = Bill.objects.order_by('-timestamp')[:5]

    # Critical stock products for quick alert widget
    critical_products = Product.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')[:5]

    context = {
        'today_revenue': round(float(today_revenue), 2),
        'weekly_revenue': round(float(weekly_revenue), 2),
        'monthly_revenue': round(float(monthly_revenue), 2),
        'total_bills': total_bills,
        'total_products': total_products,
        'critical_stock_count': critical_stock_count,
        'low_stock_count': low_stock_count,
        'good_stock_count': good_stock_count,
        'recent_bills': recent_bills,
        'critical_products': critical_products,
    }

    return render(request, 'dashboard/index.html', context)

@login_required
def api_revenue(request, timeframe):
    now = timezone.now()
    labels = []
    values = []

    if timeframe == 'daily':
        # 14 days
        for i in range(13, -1, -1):
            day_dt = now - timedelta(days=i)
            day_start = datetime(day_dt.year, day_dt.month, day_dt.day)
            day_end = day_start + timedelta(days=1)

            rev = Bill.objects.filter(timestamp__gte=day_start, timestamp__lt=day_end).aggregate(
                total=Sum('total_amount')
            )['total'] or 0.0

            labels.append(day_start.strftime('%d %b'))
            values.append(round(float(rev), 2))

    elif timeframe == 'weekly':
        # 8 weeks
        for i in range(7, -1, -1):
            start_dt = (now - timedelta(weeks=i + 1)) + timedelta(days=1)
            end_dt = now - timedelta(weeks=i)

            rev = Bill.objects.filter(timestamp__gte=start_dt, timestamp__lte=end_dt).aggregate(
                total=Sum('total_amount')
            )['total'] or 0.0

            labels.append(f"Wk {8 - i} ({end_dt.strftime('%d %b')})")
            values.append(round(float(rev), 2))

    elif timeframe == 'monthly':
        # 12 months
        year = now.year
        month = now.month
        month_list = []
        for _ in range(12):
            month_list.append((year, month))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        month_list.reverse()

        for yr, mo in month_list:
            start_dt = datetime(yr, mo, 1)
            if mo == 12:
                end_dt = datetime(yr + 1, 1, 1)
            else:
                end_dt = datetime(yr, mo + 1, 1)

            rev = Bill.objects.filter(timestamp__gte=start_dt, timestamp__lt=end_dt).aggregate(
                total=Sum('total_amount')
            )['total'] or 0.0

            labels.append(start_dt.strftime('%b %Y'))
            values.append(round(float(rev), 2))

    else:
        return JsonResponse({'error': 'Invalid timeframe. Use daily, weekly, or monthly.'}, status=400)

    return JsonResponse({
        'labels': labels,
        'values': values
    })

@login_required
def api_category_sales(request):
    sales_map = {cat: 0.0 for cat in CATEGORIES}

    items = BillItem.objects.filter(product__isnull=False).select_related('product')
    for item in items:
        cat = item.product.category
        if cat in sales_map:
            sales_map[cat] += float(item.quantity * item.price_at_sale)
        else:
            sales_map[cat] = float(item.quantity * item.price_at_sale)

    for k in sales_map:
        sales_map[k] = round(sales_map[k], 2)

    return JsonResponse({
        'labels': list(sales_map.keys()),
        'values': list(sales_map.values())
    })

@login_required
def api_top_products(request):
    results = (
        BillItem.objects.values('product_name')
        .annotate(
            revenue=Sum(F('quantity') * F('price_at_sale')),
            units=Sum('quantity')
        )
        .order_by('-revenue')[:5]
    )

    labels = []
    revenues = []
    units = []

    for r in results:
        labels.append(r['product_name'])
        revenues.append(round(float(r['revenue'] or 0.0), 2))
        units.append(int(r['units'] or 0))

    return JsonResponse({
        'labels': labels,
        'revenues': revenues,
        'units': units
    })

def custom_404_view(request, exception=None):
    return render(request, 'base.html', {'not_found': True}, status=404)
