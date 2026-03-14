"""
Subscription admin configuration
"""
from django.contrib import admin
from .models import MembershipPlan, Subscription


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'duration_days', 'price', 'registration_fee',
        'max_freeze_days', 'is_active', 'display_order', 'created_at'
    ]
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['display_order', 'price']
    
    fieldsets = (
        ('Plan Details', {
            'fields': ('name', 'description', 'display_order')
        }),
        ('Duration & Pricing', {
            'fields': ('duration_days', 'price', 'registration_fee')
        }),
        ('Features', {
            'fields': ('features', 'max_freeze_days')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'member', 'plan', 'start_date', 'end_date',
        'status', 'amount_paid', 'auto_renew', 'created_at'
    ]
    list_filter = ['status', 'auto_renew', 'start_date', 'end_date']
    search_fields = [
        'member__member_code', 'member__first_name',
        'member__last_name', 'plan__name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']
    
    fieldsets = (
        ('Subscription Info', {
            'fields': ('member', 'plan')
        }),
        ('Period', {
            'fields': ('start_date', 'end_date', 'status')
        }),
        ('Pricing', {
            'fields': ('amount_paid', 'discount', 'payment')
        }),
        ('Freeze Management', {
            'fields': (
                'freeze_start_date', 'freeze_end_date', 'freeze_days_used'
            )
        }),
        ('Settings', {
            'fields': ('auto_renew', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )