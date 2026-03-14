"""
Subscription signals
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Subscription
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Subscription)
def subscription_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for subscription creation/update
    """
    if created:
        logger.info(
            f"New subscription created: {instance.member.member_code} - "
            f"{instance.plan.name} ({instance.start_date} to {instance.end_date})"
        )
    
    # Log status changes
    if not created:
        logger.info(
            f"Subscription updated: {instance.member.member_code} - "
            f"Status: {instance.status}"
        )