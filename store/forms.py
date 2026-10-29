from django import forms

CATEGORIES = [
    ('Vegetables', 'Vegetables'),
    ('Fruits', 'Fruits'),
    ('Grocery', 'Grocery'),
    ('Electronics', 'Electronics'),
    ('Toiletries', 'Toiletries'),
    ('Decor', 'Decor'),
    ('Kitchen', 'Kitchen'),
]

ROLES = [
    ('cashier', 'Cashier'),
    ('manager', 'Store Manager'),
    ('admin', 'Administrator'),
]

class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@quickmart.com', 'autofocus': True})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )
    remember = forms.BooleanField(required=False)

class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rahul Sharma', 'autofocus': True})
    )
    email = forms.EmailField(
        max_length=120,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@quickmart.com'})
    )
    role = forms.ChoiceField(
        choices=ROLES,
        required=True,
        initial='cashier',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        min_length=6,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Min. 6 characters'})
    )
    confirm_password = forms.CharField(
        min_length=6,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'})
    )
    category = forms.ChoiceField(
        choices=CATEGORIES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    price = forms.FloatField(
        min_value=0.0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'})
    )
    stock_quantity = forms.IntegerField(
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    supplier_id = forms.IntegerField(required=False)

class SupplierForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Company / Name'})
    )
    contact_person = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person'})
    )
    phone = forms.CharField(
        max_length=25,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'})
    )
    email = forms.EmailField(
        max_length=120,
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vendor@example.com'})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Warehouse address'})
    )
