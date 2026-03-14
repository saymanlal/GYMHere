"""
Members URL configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'members'

router = DefaultRouter()
router.register(r'', views.MemberViewSet, basename='member')
router.register(r'leads', views.LeadViewSet, basename='lead')

urlpatterns = [
    path('', include(router.urls)),
]