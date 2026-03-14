"""
Member signals
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Member, Lead
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Member)
def member_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for member creation/update
    """
    if created:
        logger.info(f"New member created: {instance.member_code} - {instance.full_name}")
    else:
        logger.info(f"Member updated: {instance.member_code}")


@receiver(post_save, sender=Lead)
def lead_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for lead creation/update
    """
    if created:
        logger.info(f"New lead created: {instance.full_name}")
    
    # Log conversion
    if instance.status == 'converted' and instance.converted_to_member:
        logger.info(f"Lead {instance.full_name} converted to member {instance.converted_to_member.member_code}")