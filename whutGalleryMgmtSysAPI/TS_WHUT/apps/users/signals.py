from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Org


@receiver(post_save, sender=Org)
def create_org(sender, instance=None, created=False, **kwargs):
    """
    当认证状态改变时
    """
    if instance.status == '2':
        user = instance.user
        user.if_cer = True
        user.org_name = instance.name
        user.save()
