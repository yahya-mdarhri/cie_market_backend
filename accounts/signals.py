
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from inventors.models import Inventor

# Sync User.email → Inventor.email
@receiver(post_save, sender=User)
def sync_user_email_to_inventor(sender, instance, **kwargs):
    if instance.inventor and instance.email != instance.inventor.email:
        instance.inventor.email = instance.email
        instance.inventor.save(update_fields=['email'])

# Sync Inventor.email → User.email
@receiver(post_save, sender=Inventor)
def sync_inventor_email_to_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(inventor=instance)
        if user.email != instance.email:
            user.email = instance.email
            user.save(update_fields=['email'])
    except User.DoesNotExist:
        pass