import json
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.urls import reverse
from django.db import transaction
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from store.models import Bill, BillItem, Product
from store.views.auth_views import login_required

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def generate_bill_number():
    now = timezone.now()
    prefix = f"QM-{now.strftime('%Y%m')}-"
    count = Bill.objects.filter(bill_number__startswith=prefix).count() + 1
    while True:
        candidate = f"{prefix}{count:04d}"
        if not Bill.objects.filter(bill_number=candidate).exists():
            return candidate
        count += 1

@login_required
def index(request):
    bills = Bill.objects.prefetch_related('items').order_by('-timestamp')[:50]
    return render(request, 'billing/index.html', {'bills': bills})

@login_required
def new_bill(request):
    products = Product.objects.order_by('category', 'name')
    categories = sorted(list(set(p.category for p in products)))
    return render(request, 'billing/new_bill.html', {'products': products, 'categories': categories})

@csrf_exempt
@login_required
def create(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'POST method required.'}), 405

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'message': 'Invalid JSON request payload.'}), 400

    customer_name = (data.get('customer_name') or '').strip()
    customer_mobile = (data.get('customer_mobile') or '').strip()
    payment_method = (data.get('payment_method') or 'Cash').strip()
    items_data = data.get('items', [])

    if not customer_name:
        return JsonResponse({'success': False, 'message': 'Customer name is required.'}), 400

    if not customer_mobile:
        return JsonResponse({'success': False, 'message': 'Customer mobile number is required.'}), 400

    if not items_data or len(items_data) == 0:
        return JsonResponse({'success': False, 'message': 'Cart is empty. Please add at least one product.'}), 400

    # Stock validation and calculation
    subtotal = 0.0
    processed_items = []

    for item in items_data:
        p_id = item.get('product_id')
        qty = item.get('quantity', 0)

        try:
            qty = int(qty)
            if qty <= 0:
                return JsonResponse({'success': False, 'message': 'Invalid item quantity.'}), 400
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'message': 'Invalid item quantity format.'}), 400

        try:
            product = Product.objects.get(id=p_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': f'Product ID {p_id} not found.'}), 404

        if product.stock_quantity < qty:
            return JsonResponse({
                'success': False,
                'message': f'Insufficient stock for "{product.name}". Available: {product.stock_quantity}, Requested: {qty}.'
            }), 400

        item_total = float(product.price) * qty
        subtotal += item_total
        processed_items.append({
            'product': product,
            'quantity': qty,
            'price': float(product.price),
            'name': product.name
        })

    # Tax calculation: SGST 9% + CGST 9%
    subtotal = round(subtotal, 2)
    sgst = round(subtotal * 0.09, 2)
    cgst = round(subtotal * 0.09, 2)
    total_amount = round(subtotal + sgst + cgst, 2)

    bill_number = generate_bill_number()

    with transaction.atomic():
        bill = Bill(
            bill_number=bill_number,
            customer_name=customer_name,
            customer_mobile=customer_mobile,
            subtotal=subtotal,
            sgst=sgst,
            cgst=cgst,
            total_amount=total_amount,
            payment_method=payment_method,
            timestamp=timezone.now()
        )
        bill.save()

        for item in processed_items:
            product = item['product']
            bill_item = BillItem(
                bill=bill,
                product=product,
                product_name=item['name'],
                quantity=item['quantity'],
                price_at_sale=item['price']
            )
            bill_item.save()

            # Decrement product stock
            product.stock_quantity -= item['quantity']
            product.save()

    return JsonResponse({
        'success': True,
        'message': 'Bill generated successfully!',
        'bill_id': bill.id,
        'bill_number': bill.bill_number,
        'redirect_url': reverse('billing:receipt', kwargs={'id': bill.id})
    })

@login_required
def receipt(request, id):
    bill = get_object_or_404(Bill.objects.prefetch_related('items'), id=id)
    return render(request, 'billing/receipt.html', {'bill': bill})

@login_required
def generate_pdf(request, id):
    bill = get_object_or_404(Bill.objects.prefetch_related('items'), id=id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom palette colors matching project
    orange = colors.HexColor('#E87F24')
    blue = colors.HexColor('#73A5CA')
    dark = colors.HexColor('#1E293B')
    cream = colors.HexColor('#FEFDDF')
    light_gray = colors.HexColor('#F8FAFC')
    border_gray = colors.HexColor('#E2E8F0')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=orange,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    tagline_style = ParagraphStyle(
        'DocTagline',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=dark,
        alignment=TA_CENTER,
        spaceAfter=15
    )

    normal_style = ParagraphStyle(
        'DocNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=dark,
        leading=12
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    # Header
    story.append(Paragraph("QUICK MART", title_style))
    story.append(Paragraph("Retail Store Management System &bull; Tax Invoice", tagline_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=orange, spaceAfter=15))

    cashier_name = request.user.name if getattr(request.user, 'name', None) else 'Store Cashier'

    # Bill Info Grid
    info_data = [
        [
            Paragraph(f"<b>Bill Number:</b> {bill.bill_number}", normal_style),
            Paragraph(f"<b>Date:</b> {bill.formatted_date}", normal_style)
        ],
        [
            Paragraph(f"<b>Customer Name:</b> {bill.customer_name}", normal_style),
            Paragraph(f"<b>Payment Method:</b> {bill.payment_method}", normal_style)
        ],
        [
            Paragraph(f"<b>Customer Mobile:</b> {bill.customer_mobile}", normal_style),
            Paragraph(f"<b>Cashier:</b> {cashier_name}", normal_style)
        ]
    ]

    info_table = Table(info_data, colWidths=[270, 270])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_gray),
        ('BOX', (0, 0), (-1, -1), 0.5, border_gray),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))

    # Items Table
    table_rows = [
        [
            Paragraph("<b>#</b>", table_header_style),
            Paragraph("<b>Product Description</b>", table_header_style),
            Paragraph("<b>Unit Price (₹)</b>", table_header_style),
            Paragraph("<b>Qty</b>", table_header_style),
            Paragraph("<b>Total (₹)</b>", table_header_style)
        ]
    ]

    for idx, item in enumerate(bill.items.all(), start=1):
        table_rows.append([
            Paragraph(str(idx), normal_style),
            Paragraph(item.product_name, normal_style),
            Paragraph(f"₹{item.price_at_sale:.2f}", normal_style),
            Paragraph(str(item.quantity), normal_style),
            Paragraph(f"₹{item.total_price:.2f}", normal_style)
        ])

    items_table = Table(table_rows, colWidths=[30, 240, 90, 60, 120])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), blue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_gray),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray])
    ]))
    story.append(items_table)
    story.append(Spacer(1, 15))

    # Summary Table
    summary_data = [
        [Paragraph("<b>Subtotal:</b>", normal_style), Paragraph(f"₹{bill.subtotal:.2f}", normal_style)],
        [Paragraph("<b>SGST (9.0%):</b>", normal_style), Paragraph(f"₹{bill.sgst:.2f}", normal_style)],
        [Paragraph("<b>CGST (9.0%):</b>", normal_style), Paragraph(f"₹{bill.cgst:.2f}", normal_style)],
        [
            Paragraph("<b>GRAND TOTAL:</b>", ParagraphStyle('TotLabel', parent=normal_style, fontName='Helvetica-Bold', fontSize=12, textColor=orange)),
            Paragraph(f"<b>₹{bill.total_amount:.2f}</b>", ParagraphStyle('TotVal', parent=normal_style, fontName='Helvetica-Bold', fontSize=12, textColor=orange))
        ]
    ]

    summary_table = Table(summary_data, colWidths=[140, 120], hAlign='RIGHT')
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('LINEABOVE', (0, 3), (1, 3), 1, orange),
        ('BACKGROUND', (0, 3), (1, 3), cream)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 25))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER
    )
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_gray, spaceAfter=8))
    story.append(Paragraph("Thank you for shopping at Quick Mart! Please visit again.", footer_style))
    story.append(Paragraph("Goods once sold can be exchanged within 7 days with original receipt.", footer_style))

    doc.build(story)
    buffer.seek(0)

    filename = f"receipt_{bill.bill_number}.pdf"
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/pdf'
    )
