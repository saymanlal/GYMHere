"""
Subscription views
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from .models import MembershipPlan, Subscription
from .serializers import (
    MembershipPlanSerializer, MembershipPlanListSerializer,
    SubscriptionSerializer, SubscriptionListSerializer,
    CreateSubscriptionSerializer, FreezeSubscriptionSerializer,
    RenewSubscriptionSerializer
)
from core.exceptions import success_response


class MembershipPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Membership Plan CRUD operations
    """
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['display_order', 'price', 'duration_days', 'created_at']
    ordering = ['display_order', 'price']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return MembershipPlanListSerializer
        return MembershipPlanSerializer
    
    def list(self, request, *args, **kwargs):
        """List all membership plans"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Get single plan details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create new membership plan"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            serializer.data,
            message="Membership plan created successfully",
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update membership plan"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            serializer.data,
            message="Membership plan updated successfully"
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete membership plan"""
        instance = self.get_object()
        
        # Check if plan has active subscriptions
        active_subs = instance.subscriptions.filter(status='active').count()
        if active_subs > 0:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'PLAN_IN_USE',
                        'message': f'Cannot delete plan with {active_subs} active subscriptions'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.delete()
        return success_response(
            None,
            message="Membership plan deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active plans"""
        plans = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(plans, many=True)
        return success_response(serializer.data)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Subscription CRUD operations
    """
    queryset = Subscription.objects.select_related('member', 'plan', 'payment')
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'member', 'plan']
    search_fields = ['member__member_code', 'member__first_name', 'member__last_name']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-start_date']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return SubscriptionListSerializer
        elif self.action == 'create':
            return CreateSubscriptionSerializer
        elif self.action == 'freeze':
            return FreezeSubscriptionSerializer
        elif self.action == 'renew':
            return RenewSubscriptionSerializer
        return SubscriptionSerializer
    
    def list(self, request, *args, **kwargs):
        """List all subscriptions with pagination"""
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
        """Get single subscription details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create new subscription"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        
        # Return full subscription data
        response_serializer = SubscriptionSerializer(subscription)
        return success_response(
            response_serializer.data,
            message="Subscription created successfully",
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update subscription"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            serializer.data,
            message="Subscription updated successfully"
        )
    
    @action(detail=True, methods=['post'])
    def freeze(self, request, pk=None):
        """Freeze subscription"""
        subscription = self.get_object()
        
        if subscription.status != 'active':
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'INVALID_STATUS',
                        'message': 'Only active subscriptions can be frozen'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(
            data=request.data,
            context={'subscription': subscription}
        )
        serializer.is_valid(raise_exception=True)
        
        try:
            subscription.freeze(
                days=serializer.validated_data['days'],
                start_date=serializer.validated_data.get('start_date')
            )
            
            response_serializer = SubscriptionSerializer(subscription)
            return success_response(
                response_serializer.data,
                message="Subscription frozen successfully"
            )
        except ValueError as e:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'FREEZE_FAILED',
                        'message': str(e)
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def unfreeze(self, request, pk=None):
        """Unfreeze subscription"""
        subscription = self.get_object()
        
        if subscription.status != 'frozen':
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'NOT_FROZEN',
                        'message': 'Subscription is not frozen'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription.unfreeze()
        serializer = SubscriptionSerializer(subscription)
        return success_response(
            serializer.data,
            message="Subscription unfrozen successfully"
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel subscription"""
        subscription = self.get_object()
        subscription.cancel()
        
        serializer = SubscriptionSerializer(subscription)
        return success_response(
            serializer.data,
            message="Subscription cancelled successfully"
        )
    
    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        """Renew subscription"""
        subscription = self.get_object()
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment_id = serializer.validated_data.get('payment_id')
        payment = None
        if payment_id:
            from payments.models import Payment
            payment = Payment.objects.get(id=payment_id)
        
        new_subscription = subscription.renew(payment=payment)
        
        response_serializer = SubscriptionSerializer(new_subscription)
        return success_response(
            response_serializer.data,
            message="Subscription renewed successfully"
        )
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get subscriptions expiring soon"""
        days = int(request.query_params.get('days', 7))
        today = timezone.now().date()
        cutoff_date = today + timedelta(days=days)
        
        subscriptions = self.queryset.filter(
            status='active',
            end_date__lte=cutoff_date,
            end_date__gte=today
        )
        
        serializer = SubscriptionListSerializer(subscriptions, many=True)
        return success_response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get subscription statistics"""
        total = Subscription.objects.count()
        active = Subscription.objects.filter(status='active').count()
        expired = Subscription.objects.filter(status='expired').count()
        frozen = Subscription.objects.filter(status='frozen').count()
        cancelled = Subscription.objects.filter(status='cancelled').count()
        
        today = timezone.now().date()
        expiring_7_days = Subscription.objects.filter(
            status='active',
            end_date__lte=today + timedelta(days=7),
            end_date__gte=today
        ).count()
        
        stats_data = {
            'total': total,
            'active': active,
            'expired': expired,
            'frozen': frozen,
            'cancelled': cancelled,
            'expiring_soon': expiring_7_days,
        }
        
        return success_response(stats_data)