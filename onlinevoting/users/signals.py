from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Member

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender = User)
def create_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user = instance)

def save_member(sender, instance, **kwargs):
    instance.member.save()
