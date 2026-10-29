from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from store.models import Supplier, Product
from store.views.auth_views import login_required

@login_required
def index(request):
    search = request.GET.get('search', '').strip()
    query = Supplier.objects.prefetch_related('products')

    if search:
        query = query.filter(
            Q(name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    suppliers = query.order_by('name')
    return render(request, 'suppliers/index.html', {'suppliers': suppliers, 'search_query': search})

@login_required
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if not name:
            messages.error(request, 'Supplier Company / Name is required.')
            return redirect('suppliers:index')

        supplier = Supplier(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address
        )
        supplier.save()

        messages.success(request, f'Supplier "{name}" registered successfully.')
        return redirect('suppliers:index')

    return redirect('suppliers:index')

@login_required
def edit(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()

        if not name:
            messages.error(request, 'Supplier Company / Name is required.')
            return render(request, 'suppliers/edit.html', {'supplier': supplier})

        supplier.name = name
        supplier.contact_person = contact_person
        supplier.phone = phone
        supplier.email = email
        supplier.address = address
        supplier.save()

        messages.success(request, f'Supplier "{name}" updated successfully.')
        return redirect('suppliers:index')

    return render(request, 'suppliers/edit.html', {'supplier': supplier})

@login_required
def delete(request, id):
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, id=id)
        name = supplier.name

        # Unlink products supplied by this supplier before deletion
        Product.objects.filter(supplier=supplier).update(supplier=None)

        supplier.delete()
        messages.info(request, f'Supplier "{name}" has been removed.')

    return redirect('suppliers:index')
