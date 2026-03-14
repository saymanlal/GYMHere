"""
Subscription serializers
"""
from rest_framework import serializers
from .models import MembershipPlan, Subscription
from members.serializers import MemberListSerializer


class MembershipPlanSerializer(serializers.ModelSerializer):
    """
    Membership Plan serializer
    """
    duration_months = serializers.IntegerField(read_only=True)
    price_per_month = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = MembershipPlan
        fields = [
            'id', 'name', 'description', 'duration_days', 'duration_months',
            'price', 'price_per_month', 'registration_fee', 'features',
            'max_freeze_days', 'is_active', 'display_order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MembershipPlanListSerializer(serializers.ModelSerializer):
    """
    Simplified plan serializer for list view
    """
    duration_months = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = MembershipPlan
        fields = [
            'id', 'name', 'duration_days', 'duration_months',
            'price', 'is_active'
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Subscription serializer
    """
    member = MemberListSerializer(read_only=True)
    member_id = serializers.UUIDField(write_only=True)
    plan = MembershipPlanSerializer(read_only=True)
    plan_id = serializers.UUIDField(write_only=True)
    
    is_active = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    is_expiring_soon = serializers.BooleanField(read_only=True)
    freeze_days_remaining = serializers.IntegerField(read_only=True)
    is_frozen = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'member', 'member_id', 'plan', 'plan_id',
            'start_date', 'end_date', 'amount_paid', 'discount',
            'status', 'payment', 'freeze_start_date', 'freeze_end_date',
            'freeze_days_used', 'auto_renew', 'notes',
            'is_active', 'is_expired', 'days_remaining', 'is_expiring_soon',
            'freeze_days_remaining', 'is_frozen',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'status', 'freeze_start_date', 'freeze_end_date',
            'freeze_days_used', 'created_at', 'updated_at'
        ]
    
    def validate(self, attrs):
        """Validate subscription dates"""
        if 'start_date' in attrs and 'end_date' in attrs:
            if attrs['end_date'] <= attrs['start_date']:
                raise serializers.ValidationError(
                    "End date must be after start date"
                )
        return attrs


class SubscriptionListSerializer(serializers.ModelSerializer):
    """
    Simplified subscription serializer for list view
    """
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    member_code = serializers.CharField(source='member.member_code', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'member_code', 'member_name', 'plan_name',
            'start_date', 'end_date', 'status', 'days_remaining'
        ]


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for creating subscriptions
    """
    class Meta:
        model = Subscription
        fields = [
            'member_id', 'plan_id', 'start_date', 'end_date',
            'amount_paid', 'discount', 'auto_renew', 'notes'
        ]
    
    def create(self, validated_data):
        """Create subscription and update member status"""
        from members.models import Member
        
        member_id = validated_data.pop('member_id')
        plan_id = validated_data.pop('plan_id')
        
        member = Member.objects.get(id=member_id)
        plan = MembershipPlan.objects.get(id=plan_id)
        
        subscription = Subscription.objects.create(
            member=member,
            plan=plan,
            **validated_data
        )
        
        return subscription


class FreezeSubscriptionSerializer(serializers.Serializer):
    """
    Serializer for freezing subscription
    """
    days = serializers.IntegerField(min_value=1)
    start_date = serializers.DateField(required=False)
    
    def validate_days(self, value):
        """Validate freeze days against plan limit"""
        subscription = self.context['subscription']
        if value > subscription.freeze_days_remaining:
            raise serializers.ValidationError(
                f"Only {subscription.freeze_days_remaining} freeze days remaining"
            )
        return value


class RenewSubscriptionSerializer(serializers.Serializer):
    """
    Serializer for renewing subscription
    """
    payment_id = serializers.UUIDField(required=False, allow_null=True)
    discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        default=0
    )