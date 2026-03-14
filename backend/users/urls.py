"""
Users URL configuration
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('me/', views.me_view, name='me'),
    path('me/update/', views.update_profile_view, name='update_profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # Password reset
    path('reset-password/', views.password_reset_view, name='password_reset'),
    path('reset-password/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
]