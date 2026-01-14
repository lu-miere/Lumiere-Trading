from django.db import models
from django.contrib.contenttypes.models import ContentType
from .models.account_models import SharedAccess

class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f'{self.title}'

class AccountTimeMixin(models.Model):
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionMixin(TimeMixin, models.Model):
    class Meta:
        abstract = True

    @property
    def shared_users(self):
        ct = ContentType.objects.get_for_model(self)
        return SharedAccess.objects.filter(content_type= ct, content_id = self.id)
    
    def grant_permission(self, user, role, grantor):
        ct = ContentType.objects.get_for_model(self)
        return SharedAccess.objects.update_or_create(
            content_type = ct,
            content_id = self.id,
            user = user,
            defaults={'role': role, 'granted_by': grantor}
        )
