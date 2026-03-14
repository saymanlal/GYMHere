"""
Member serializers
"""
from rest_framework import serializers
from .models import Member, Lead
from users.serializers import UserSerializer


class MemberSerializer(serializers.ModelSerializer):
    """
    Member serializer
    """
    user = UserSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    has_active_subscription = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Member
        fields = [
            'id', 'user', 'member_code', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'postal_code',
            'emergency_contact_name', 'emergency_contact_phone',
            'blood_group', 'medical_conditions', 'profile_photo',
            'status', 'joined_date', 'notes', 'full_name', 'age',
            'has_active_subscription', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'member_code', 'joined_date', 'created_at', 'updated_at']
    
    def validate_phone(self, value):
        """Validate phone number"""
        if Member.objects.filter(phone=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A member with this phone number already exists.")
        return value
    
    def validate_email(self, value):
        """Validate email"""
        if value and Member.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A member with this email already exists.")
        return value


class MemberListSerializer(serializers.ModelSerializer):
    """
    Simplified member serializer for list view
    """
    full_name = serializers.CharField(read_only=True)
    has_active_subscription = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Member
        fields = [
            'id', 'member_code', 'full_name', 'email', 'phone',
            'status', 'joined_date', 'has_active_subscription'
        ]


class MemberCreateSerializer(serializers.ModelSerializer):
    """
    Member creation serializer
    """
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'postal_code',
            'emergency_contact_name', 'emergency_contact_phone',
            'blood_group', 'medical_conditions', 'notes'
        ]
    
    def create(self, validated_data):
        """Create member with auto-generated member code"""
        member = Member.objects.create(**validated_data)
        return member


class LeadSerializer(serializers.ModelSerializer):
    """
    Lead serializer
    """
    full_name = serializers.CharField(read_only=True)
    assigned_to_name = serializers.SerializerMethodField()
    interested_plan_name = serializers.SerializerMethodField()
    converted_member_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'source', 'status', 'interested_plan', 'interested_plan_name',
            'assigned_to', 'assigned_to_name', 'follow_up_date', 'notes',
            'converted_to_member', 'converted_member_name',
            'full_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_assigned_to_name(self, obj):
        return obj.assigned_to.full_name if obj.assigned_to else None
    
    def get_interested_plan_name(self, obj):
        return obj.interested_plan.name if obj.interested_plan else None
    
    def get_converted_member_name(self, obj):
        return obj.converted_to_member.full_name if obj.converted_to_member else None


class LeadListSerializer(serializers.ModelSerializer):
    """
    Simplified lead serializer for list view
    """
    full_name = serializers.CharField(read_only=True)
    assigned_to_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Lead
        fields = [
            'id', 'full_name', 'phone', 'email', 'source',
            'status', 'assigned_to_name', 'follow_up_date', 'created_at'
        ]
    
    def get_assigned_to_name(self, obj):
        return obj.assigned_to.full_name if obj.assigned_to else None


class LeadConvertSerializer(serializers.Serializer):
    """
    Serializer for converting lead to member
    """
    member_data = MemberCreateSerializer()
    
    def create(self, validated_data):
        """Convert lead to member"""
        member_data = validated_data['member_data']
        lead = self.context['lead']
        
        # Create member from lead data
        member = Member.objects.create(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
            **member_data
        )
        
        # Update lead
        lead.convert_to_member(member)
        
        return member