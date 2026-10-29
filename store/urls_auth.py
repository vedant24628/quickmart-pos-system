from django.urls import path
from store.views.auth_views import login_view, register_view, logout_view

app_name = 'auth'

urlpatterns = [
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
]
