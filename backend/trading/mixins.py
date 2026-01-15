from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

User = settings.AUTH_USER_MODEL

class TimeMixin(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f'{self.title}'
    
    class Meta:
         abstract = True

class AccountTimeMixin(models.Model):
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
         abstract = True

class SharedAccess(TimeMixin, models.Model):
    
    class ROLES(models.TextChoices):
        VIEWER = 'VIEWER', 'View-only'
        COMMENTER = 'COMMENTER', 'Can comment but not edit'
        EDITOR = 'EDITOR', 'Can edit content'
        ADMIN = 'ADMIN', 'Full control including resharing'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='granted_access')
    role = models.CharField(max_length=15, choices=ROLES.choices, default = ROLES.VIEWER)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')

    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions_given')

    class Meta:
        unique_together = ('user', 'content_type', 'content_id')
        verbose_name = 'Shared Access'
        indexes = [
            models.Index(fields=['content_type','content_id'])
        ]

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

class Comments(TimeMixin, models.Model):
    user = models.ForeignKey(on_delete=models.CASCADE, null= True, related_name='comments')
    text = models.TextField(max_length=500, null= False, blank=False, help_text='comment')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['content_type', 'content_id'])
        ]
         
class CommentsMixin(models.Model):
    def comments(self, user):
        ct = ContentType.objects.get_for_model(self)
        return Comments.objects.filter(user = user)
    
    def add_or_update_comment(self, user, entry_id):
        ct = ContentType.objects.get_for_model(self)
        return Comments.objects.update_or_create(
            user = user,
            content_type = ct,
            content_id = entry_id
            
        )
    class Meta:
        abstract = True
    
class PsychologyMatrix(models.Model):
        class MoodScores(models.IntegerChoices):
            pass
      
        class TradeResults(models.TextChoices):
            pass
      


class FundamentalsEntryMixin(models.Model):
    class PriorityLevel(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, "High"
    class SessionType(models.TextChoices):
        NY = "NY", "New York"
        TKYO =  "TKYO", "Tokyo"
        LON = "LON", "London"
    
    priority = models.IntegerField(choices=PriorityLevel, default=PriorityLevel.LOW)
    comments = models.ManyToOneRel(Comments, null = True, blank = True)
    session = models.CharField(choices = SessionType.choices, null = True, blank= True, verbose_name="Trading Session")

    class Meta:
         abstract = True
         