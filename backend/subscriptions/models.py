"""
Subscription and Membership Plan models
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


class MembershipPlan(models.Model):
    """
    Membership Plan model - Defines available membership packages
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Plan Details
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Duration and Pricing
    duration_days = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Plan duration in days (e.g., 30, 90, 180, 365)"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Features
    features = models.JSONField(
        default=list,
        help_text="Array of features included in this plan"
    )
    
    # Freeze Policy
    max_freeze_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Maximum days member can freeze this subscription"
    )
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    
    # Display Order
    display_order = models.IntegerField(default=0, help_text="Order for displaying plans")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'membership_plans'
        ordering = ['display_order', 'price']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['display_order']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.duration_days} days)"
    
    @property
    def duration_months(self):
        """Get approximate duration in months"""
        return round(self.duration_days / 30)
    
    @property
    def price_per_month(self):
        """Calculate approximate price per month"""
        months = max(self.duration_days / 30, 1)
        return round(self.price / months, 2)


class Subscription(models.Model):
    """
    Subscription model - Member's active/past subscriptions
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('frozen', 'Frozen'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    
    # Subscription Period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Pricing
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_index=True
    )
    
    # Payment Reference
    payment = models.ForeignKey(
        'payments.Payment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions'
    )
    
    # Freeze Management
    freeze_start_date = models.DateField(null=True, blank=True)
    freeze_end_date = models.DateField(null=True, blank=True)
    freeze_days_used = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Auto Renewal
    auto_renew = models.BooleanField(default=False)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['member']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['end_date']),
        ]
    
    def __str__(self):
        return f"{self.member.member_code} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        today = timezone.now().date()
        return (
            self.status == 'active' and
            self.start_date <= today <= self.end_date
        )
    
    @property
    def is_expired(self):
        """Check if subscription has expired"""
        today = timezone.now().date()
        return today > self.end_date
    
    @property
    def days_remaining(self):
        """Calculate days remaining in subscription"""
        if self.status == 'frozen':
            return None
        today = timezone.now().date()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days
    
    @property
    def is_expiring_soon(self, days=7):
        """Check if subscription is expiring within specified days"""
        remaining = self.days_remaining
        return remaining is not None and 0 < remaining <= days
    
    @property
    def freeze_days_remaining(self):
        """Calculate remaining freeze days available"""
        return max(self.plan.max_freeze_days - self.freeze_days_used, 0)
    
    @property
    def is_frozen(self):
        """Check if subscription is currently frozen"""
        return self.status == 'frozen'
    
    def can_freeze(self, days):
        """Check if subscription can be frozen for given days"""
        return (
            self.status == 'active' and
            days <= self.freeze_days_remaining
        )
    
    def freeze(self, days, start_date=None):
        """Freeze subscription for specified days"""
        if not self.can_freeze(days):
            raise ValueError("Cannot freeze subscription")
        
        start = start_date or timezone.now().date()
        end = start + timedelta(days=days)
        
        self.status = 'frozen'
        self.freeze_start_date = start
        self.freeze_end_date = end
        self.freeze_days_used += days
        
        # Extend end date by freeze duration
        self.end_date += timedelta(days=days)
        self.save()
    
    def unfreeze(self):
        """Unfreeze subscription"""
        if self.status == 'frozen':
            self.status = 'active'
            self.freeze_start_date = None
            self.freeze_end_date = None
            self.save()
    
    def cancel(self):
        """Cancel subscription"""
        self.status = 'cancelled'
        self.auto_renew = False
        self.save()
    
    def renew(self, payment=None):
        """Renew subscription with same plan"""
        new_start = self.end_date + timedelta(days=1)
        new_end = new_start + timedelta(days=self.plan.duration_days)
        
        new_subscription = Subscription.objects.create(
            member=self.member,
            plan=self.plan,
            start_date=new_start,
            end_date=new_end,
            amount_paid=self.plan.price,
            payment=payment,
            auto_renew=self.auto_renew,
        )
        
        return new_subscription
    
    def save(self, *args, **kwargs):
        """Override save to update status based on dates"""
        today = timezone.now().date()
        
        # Auto-update status based on dates
        if self.status not in ['cancelled', 'frozen']:
            if today > self.end_date:
                self.status = 'expired'
            elif self.start_date <= today <= self.end_date:
                self.status = 'active'
        
        super().save(*args, **kwargs)
        
        # Update member status based on subscription
        if self.status == 'active':
            self.member.status = 'active'
            self.member.save(update_fields=['status'])
        elif self.status == 'expired' and self.member.status == 'active':
            # Only update if no other active subscriptions
            if not self.member.subscriptions.filter(status='active').exists():
                self.member.status = 'expired'
                self.member.save(update_fields=['status'])