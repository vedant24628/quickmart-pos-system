from functools import wraps
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from store.models import User

def login_required(view_func):
    """
    Decorator for views that checks if the user is authenticated,
    redirecting to the log-in page if necessary.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not getattr(request.user, 'is_authenticated', False):
            login_url = reverse('auth:login')
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_view(request):
    if getattr(request.user, 'is_authenticated', False):
        return redirect('dashboard:index')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        remember = bool(request.POST.get('remember'))

        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'auth/login.html')

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            messages.error(request, 'Invalid email address or password. Please try again.')
            return render(request, 'auth/login.html')

        request.session['user_id'] = user.id
        if not remember:
            request.session.set_expiry(0)  # expires on browser close
        else:
            request.session.set_expiry(86400 * 30)  # 30 days

        messages.success(request, f'Welcome back, {user.name}!')

        next_page = request.GET.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect('dashboard:index')

    return render(request, 'auth/login.html')

def register_view(request):
    if getattr(request.user, 'is_authenticated', False):
        return redirect('dashboard:index')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'cashier').strip()

        if not name or not email or not password:
            messages.error(request, 'All required fields must be filled out.')
            return render(request, 'auth/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'auth/register.html')

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            messages.error(request, 'An account with this email address already exists. Please log in.')
            return render(request, 'auth/register.html')

        if role not in ['cashier', 'manager', 'admin']:
            role = 'cashier'

        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        new_user.save()

        messages.success(request, 'Registration successful! You can now log in with your credentials.')
        return redirect('auth:login')

    return render(request, 'auth/register.html')

def logout_view(request):
    request.session.flush()
    messages.info(request, 'You have been logged out successfully.')
    return redirect('auth:login')
