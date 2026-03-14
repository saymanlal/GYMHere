"""
Member views
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Member, Lead
from .serializers import (
    MemberSerializer, MemberListSerializer, MemberCreateSerializer,
    LeadSerializer, LeadListSerializer, LeadConvertSerializer
)
from core.exceptions import success_response
from users.permissions import permission_required


class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Member CRUD operations
    """
    queryset = Member.objects.select_related('user').prefetch_related('subscriptions')
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'gender', 'joined_date']
    search_fields = ['member_code', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'joined_date', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return MemberListSerializer
        elif self.action == 'create':
            return MemberCreateSerializer
        return MemberSerializer
    
    def list(self, request, *args, **kwargs):
        """List all members with pagination"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data,
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Get single member details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create new member"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        
        # Return full member data
        response_serializer = MemberSerializer(member)
        return success_response(
            response_serializer.data,
            message="Member created successfully",
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update member"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            serializer.data,
            message="Member updated successfully"
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete member"""
        instance = self.get_object()
        instance.delete()
        return success_response(
            None,
            message="Member deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate member"""
        member = self.get_object()
        member.status = 'active'
        member.save()
        
        serializer = self.get_serializer(member)
        return success_response(serializer.data, message="Member activated successfully")
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate member"""
        member = self.get_object()
        member.status = 'inactive'
        member.save()
        
        serializer = self.get_serializer(member)
        return success_response(serializer.data, message="Member deactivated successfully")
    
    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """Suspend member"""
        member = self.get_object()
        member.status = 'suspended'
        member.save()
        
        serializer = self.get_serializer(member)
        return success_response(serializer.data, message="Member suspended successfully")
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get member statistics"""
        total = Member.objects.count()
        active = Member.objects.filter(status='active').count()
        inactive = Member.objects.filter(status='inactive').count()
        suspended = Member.objects.filter(status='suspended').count()
        expired = Member.objects.filter(status='expired').count()
        
        stats_data = {
            'total': total,
            'active': active,
            'inactive': inactive,
            'suspended': suspended,
            'expired': expired,
        }
        
        return success_response(stats_data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for members"""
        query = request.query_params.get('q', '')
        
        if not query:
            return success_response([])
        
        members = Member.objects.filter(
            Q(member_code__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )[:10]  # Limit to 10 results
        
        serializer = MemberListSerializer(members, many=True)
        return success_response(serializer.data)


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lead management
    """
    queryset = Lead.objects.select_related('assigned_to', 'interested_plan', 'converted_to_member')
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'source', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'follow_up_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return LeadListSerializer
        elif self.action == 'convert':
            return LeadConvertSerializer
        return LeadSerializer
    
    def list(self, request, *args, **kwargs):
        """List all leads with pagination"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data,
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create new lead"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            serializer.data,
            message="Lead created successfully",
            status_code=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        """Convert lead to member"""
        lead = self.get_object()
        
        if lead.status == 'converted':
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'ALREADY_CONVERTED',
                        'message': 'Lead has already been converted'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = LeadConvertSerializer(
            data=request.data,
            context={'lead': lead}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        
        member_serializer = MemberSerializer(member)
        return success_response(
            member_serializer.data,
            message="Lead converted to member successfully"
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get lead statistics"""
        total = Lead.objects.count()
        new = Lead.objects.filter(status='new').count()
        contacted = Lead.objects.filter(status='contacted').count()
        interested = Lead.objects.filter(status='interested').count()
        converted = Lead.objects.filter(status='converted').count()
        lost = Lead.objects.filter(status='lost').count()
        
        stats_data = {
            'total': total,
            'new': new,
            'contacted': contacted,
            'interested': interested,
            'converted': converted,
            'lost': lost,
            'conversion_rate': round((converted / total * 100) if total > 0 else 0, 2)
        }
        
        return success_response(stats_data)