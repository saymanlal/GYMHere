"""
Member models
"""
import uuid
from django.db import models
from django.core.validators import RegexValidator
from users.models import User


class Member(models.Model):
    """
    Member model - Core member information
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='member_profile')
    
    # Basic Information
    member_code = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, db_index=True)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=20)
    
    # Personal Details
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Health Information
    blood_group = models.CharField(max_length=10, blank=True)
    medical_conditions = models.TextField(blank=True, help_text="Any medical conditions or allergies")
    
    # Profile
    profile_photo = models.ImageField(upload_to='members/photos/', null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    joined_date = models.DateField(auto_now_add=True, db_index=True)
    
    # Notes
    notes = models.TextField(blank=True, help_text="Internal notes about the member")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'members'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['member_code']),
            models.Index(fields=['status']),
            models.Index(fields=['joined_date']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.member_code} - {self.full_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def active_subscription(self):
        """Get active subscription if exists"""
        return self.subscriptions.filter(status='active').first()
    
    @property
    def has_active_subscription(self):
        """Check if member has active subscription"""
        return self.subscriptions.filter(status='active').exists()
    
    def generate_member_code(self):
        """Generate unique member code"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_part = str(uuid.uuid4().hex[:6]).upper()
        return f"GYM{timestamp[-6:]}{random_part}"
    
    def save(self, *args, **kwargs):
        """Override save to generate member code"""
        if not self.member_code:
            self.member_code = self.generate_member_code()
        super().save(*args, **kwargs)


class Lead(models.Model):
    """
    Lead model - Enquiries and potential members
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('interested', 'Interested'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    SOURCE_CHOICES = [
        ('walk_in', 'Walk In'),
        ('referral', 'Referral'),
        ('online', 'Online'),
        ('social_media', 'Social Media'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    
    # Lead Details
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default='walk_in')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', db_index=True)
    
    # Interest
    interested_plan = models.ForeignKey(
        'subscriptions.MembershipPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )
    
    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )
    
    # Follow-up
    follow_up_date = models.DateField(null=True, blank=True, db_index=True)
    notes = models.TextField(blank=True)
    
    # Conversion
    converted_to_member = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lead_source'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['follow_up_date']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def convert_to_member(self, member):
        """Convert lead to member"""
        self.status = 'converted'
        self.converted_to_member = member
        self.save()