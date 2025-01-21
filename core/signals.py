from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a user profile whenever a new user is created
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure the user profile is saved if it already exists
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        pass  # If user profile doesn't exist, just ignore it
