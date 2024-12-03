from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate, sender=apps.get_app_config('menu'))
def create_user_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Gestor')
    Group.objects.get_or_create(name='Equipo de entrega')
