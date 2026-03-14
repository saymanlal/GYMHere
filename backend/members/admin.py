"""
Member admin configuration
"""
from django.contrib import admin
from .models import Member, Lead


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'member_code', 'first_name', 'last_name', 'phone', 'email',
        'status', 'joined_date', 'created_at'
    ]
    list_filter = ['status', 'gender', 'joined_date']
    search_fields = ['member_code', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['member_code', 'joined_date', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('member_code', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'profile_photo')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Health Information', {
            'fields': ('blood_group', 'medical_conditions')
        }),
        ('Status', {
            'fields': ('status', 'joined_date', 'notes')
        }),
        ('Account', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'phone', 'email',
        'source', 'status', 'assigned_to', 'follow_up_date', 'created_at'
    ]
    list_filter = ['status', 'source', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Lead Details', {
            'fields': ('source', 'status', 'interested_plan')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'follow_up_date')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Conversion', {
            'fields': ('converted_to_member',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )