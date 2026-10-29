from django.contrib import admin
from store.models import User, Supplier, Product, Bill, BillItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('role',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person', 'phone', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock_quantity', 'supplier', 'stock_status')
    search_fields = ('name', 'category')
    list_filter = ('category',)

class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 0

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'customer_name', 'customer_mobile', 'total_amount', 'payment_method', 'timestamp')
    search_fields = ('bill_number', 'customer_name', 'customer_mobile')
    list_filter = ('payment_method',)
    inlines = [BillItemInline]
