from django.db import models
from django.conf import settings
from .trading_models import Trade
from ..mixins import TimeMixin, PermissionMixin
from django.utils import timezone


User = settings.AUTH_USER_MODEL

class Comments(models.Model):
      pass

class PsychologyScore(models.Model):
      pass

class Journal(TimeMixin, models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='journal')
    date = models.DateField(default=timezone.now)
    
    comments = models.ManyToManyField(Comments, null = True, blank=True, related_name="jounral_comments")
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
        
   



class Saga (TimeMixin, PermissionMixin, models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='sagas')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
                verbose_name = 'Saga'
                verbose_name_plural = 'Sagas'


class Series(TimeMixin, models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=255)
    description = models.TextField()
    entry_date = models.DateField(default=timezone.now, null = True, blank= True, help_text='the date of the conatiner of related entries for a specificm date for a team account')

    sagas = models.ManyToManyField(Saga, blank= True, related_name= 'series' )

    class Meta:
                verbose_name = 'Serie'
                verbose_name_plural = 'Series'
                
                constraints = [
          models.UniqueConstraint(
                fields= ['user,']
          )
    ]

class Entry(TimeMixin, PermissionMixin, models.Model):
    "Single Table Based Inheritance model allows us to map different story notes to one model in the DB"
    "journal, idea, headline, econ rel"

    class EntryType(models.TextChoices):
        JOURNAL = "J", "Journal"
        IDEA =  "I", "Idea"
        NEWS = "N", "News"
        ECON = "E", "Economic"
    
    class SessionType(models.TextChoices):
        NY = "NY", "New York"
        TKYO =  "TKYO", "Tokyo"
        LON = "LON", "London"
    
    class PriorityLevel(models.IntegerChoices):
          LOW = 1, 'Low'
          MEDIUM = 2, 'Medium'
          HIGH = 3, 'High'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    entry_type = models.CharField(max_length=20, choices = EntryType.choices, default=EntryType.IDEA)
    priority = models.IntegerField(max_length=1, choices=PriorityLevel.choices, default= PriorityLevel.LOW)
    
    # related to a user journal entry
    jounral = models.OneToOneField(Journal)
    # Related series and entry date to group entries by a user selected date
    series = models.ManyToManyField(Series,  blank = True, related_name='entries')

    title = models.CharField(max_length=255, default='title')
    comments = models.TextField(null = True, blank=True)

    symbol = models.CharField(max_length=12, default = 'symbol', null = True, blank= True)
    trading_session = models.CharField(choices = SessionType.choices, null = True, blank= True, verbose_name="Trading Session")

    # Trading Journal
    entry_daily = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry Daily")
    entry_4HR = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 4H")
    entry_1H = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 1H")
    entry_30M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 30M")
    entry_15M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 15M")
    entry_5M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 5M")
    entry_1M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 1M")
    trades = models.ManyToManyField(Trade,  blank = True, related_name= 'entries')


    # News
    headline_title = models.CharField(max_length=255, null = True, blank= True, verbose_name= 'Headline Title')
    headline_url = models.URLField(max_length=500, null = True, blank= True, verbose_name= 'Headline Url')
    published_date = models.DateTimeField(verbose_name= 'Publish Date', null= True, blank= True)
    source = models.CharField(max_length=255, null= True, blank= True)
    
    # General
    extra_data = models.JSONField(default= dict, blank=True)

    @property
    def all_trades_for_day(self):
          if not self.entry_date:
                return Trade.objects.none()
          return Trade.objects.filter(
                account__user = self.user,
                entered_time__date = self.entry_date
          )

    def __str__(self):
        return f"{self.get_entry_type}  {self.title}"

    @property
    def get_entry_type(self):
        return f'{self.entry_type}'
    

    class Meta:
                verbose_name = 'Entry'
                verbose_name_plural = 'Entries'
    
 

