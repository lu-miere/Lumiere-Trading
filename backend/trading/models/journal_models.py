from django.db import models
from django.conf import settings
from .trading_models import Trade
from ..mixins import TimeMixin, PermissionMixin, SharedAccess, FundamentalsEntryMixin, Comments
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class Journal(TimeMixin, models.Model):
      user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='journal')
      date = models.DateField(default=timezone.now)
      
      pschology_rating = models.IntegerField(null=True, blank=True, help_text="rating of user's psychology")
      discipline_rating = models.IntegerField(null=True, blank=True, help_text="rating of user's psychology")

      def __str__(self):
            return f"Journal: {self.date}"

      class Meta:
            unique_together = ['user', 'date']
            verbose_name = 'journal'
            ordering = 'date'
            
      @property
      def get_day_pnl(self, start, end):
            if start and end:
                  trades = Trade.objects.filter(user = self.user)
      @property
      def all_trades_for_day(self):
            if not self.entry_date:
                  return Trade.objects.none()
            return Trade.objects.filter(
                  account__user = self.user,
                  entered_time__date = self.entry_date
            )
      
# class Saga (TimeMixin, PermissionMixin, models.Model):
#       user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='sagas')
#       title = models.CharField(max_length=255)
#       description = models.TextField()
      
#       class Meta:
#                   verbose_name = 'Saga'
#                   verbose_name_plural = 'Sagas'


class Series(TimeMixin, PermissionMixin, models.Model):
      user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='series')
      title = models.CharField(max_length=255)
      description = models.TextField()
      entry_date = models.DateField(default=timezone.now, null = True, blank= True, help_text='the date of the conatiner of related entries for a specificm date for a team account')

      class Meta:
            verbose_name = 'Serie'
            verbose_name_plural = 'Series'
                  
            constraints = [
            models.UniqueConstraint(
                  fields= ['user,']
            )
      ]

class Entry(TimeMixin, PermissionMixin, models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=255, default='title')

    class Meta:
                verbose_name = 'Entry'
                verbose_name_plural = 'Entries'

class EntryHeadline(TimeMixin, FundamentalsEntryMixin, models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="headlines")

      headline = models.CharField(max_length=255, null = True, blank= True, verbose_name= 'Headline Title')
      url = models.URLField(max_length=500, null = True, blank= True, verbose_name= 'Headline Url')
      published_date = models.DateTimeField(verbose_name= 'Publish Date', null= True, blank= True)
      source = models.CharField(max_length=255, null= True, blank= True)

class EntryEcononomic(TimeMixin, FundamentalsEntryMixin, models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="econ_cal")
      
      class Meta:
            verbose_name = 'Econ. Cal. Event'
            verbose_name_plural = 'Econ Cal Events'

      name = models.CharField(max_length= 50, null = True, blank=True, verbose_name='Econ Release Name')
      symbol = models.CharField(max_length=20, default = 'symbol', null=True, blank=True)
      release_date = models.DateField()
      actual_stat = models.IntegerField(null=True, blank=False, verbose_name='Actual Stat')
      consensus_stat = models.IntegerField(null=True, blank=False, verbose_name='Consensus Stat')
      previous_stat = models.IntegerField(null=True, blank=False, verbose_name='Previous Stat')
      country = models.CharField(max_length=25, null = True, blank=True)
