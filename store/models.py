from django.db import models
from django.utils import timezone
from store.password_utils import verify_password, hash_password

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=120, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='cashier')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'users'

    def set_password(self, password):
        self.password_hash = hash_password(password)

    def check_password(self, password):
        return verify_password(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return f'<User {self.email}>'


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'suppliers'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person or '',
            'phone': self.phone or '',
            'email': self.email or '',
            'address': self.address or '',
            'product_count': self.products.count()
        }

    def __str__(self):
        return f'<Supplier {self.name}>'


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    price = models.FloatField()
    stock_quantity = models.IntegerField(default=0)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='supplier_id',
        related_name='products'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'products'

    @property
    def stock_status(self):
        if self.stock_quantity < 10:
            return 'status-critical'
        elif self.stock_quantity <= 30:
            return 'status-low'
        return 'status-good'

    @property
    def stock_label(self):
        if self.stock_quantity < 10:
            return 'Critical'
        elif self.stock_quantity <= 30:
            return 'Low Stock'
        return 'In Stock'

    @property
    def formatted_price(self):
        return f"{self.price:,.2f}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': round(float(self.price), 2),
            'stock_quantity': int(self.stock_quantity),
            'supplier_name': self.supplier.name if self.supplier else 'None',
            'stock_status': self.stock_status,
            'stock_label': self.stock_label
        }

    def __str__(self):
        return f'<Product {self.name} - Qty: {self.stock_quantity}>'


class Bill(models.Model):
    bill_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_mobile = models.CharField(max_length=25)
    subtotal = models.FloatField()
    sgst = models.FloatField()
    cgst = models.FloatField()
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=30, default='Cash')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'bills'

    @property
    def formatted_total(self):
        return f"{self.total_amount:,.2f}"

    @property
    def formatted_date(self):
        if self.timestamp:
            return self.timestamp.strftime('%d-%b-%Y %I:%M %p')
        return ''

    def to_dict(self):
        return {
            'id': self.id,
            'bill_number': self.bill_number,
            'customer_name': self.customer_name,
            'customer_mobile': self.customer_mobile,
            'subtotal': round(float(self.subtotal), 2),
            'sgst': round(float(self.sgst), 2),
            'cgst': round(float(self.cgst), 2),
            'total_amount': round(float(self.total_amount), 2),
            'payment_method': self.payment_method,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else '',
            'item_count': self.items.count()
        }

    def __str__(self):
        return f'<Bill {self.bill_number} - ₹{self.total_amount}>'


class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        db_column='bill_id',
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='product_id',
        related_name='bill_items'
    )
    product_name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    price_at_sale = models.FloatField()

    class Meta:
        managed = False
        db_table = 'bill_items'

    @property
    def total_price(self):
        return round(float(self.quantity * self.price_at_sale), 2)

    @property
    def formatted_total_price(self):
        return f"{self.total_price:,.2f}"

    def to_dict(self):
        return {
            'id': self.id,
            'bill_id': self.bill_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price_at_sale': round(float(self.price_at_sale), 2),
            'total_price': self.total_price
        }

    def __str__(self):
        return f'<BillItem {self.product_name} x {self.quantity}>'
