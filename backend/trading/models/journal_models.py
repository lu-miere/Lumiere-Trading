from django.db import models
from django.conf import settings
from .trading_models import Trade

User = settings.AUTH_USER_MODEL

class Saga (models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_sagas')
    title = models.CharField(max_length=255)
    description = models.TextField()
    shared_with = models.ManyToManyField(User, through='SagaMembership', blank= True)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f'{self.title}'

class SagaMembership(models.Model):
    "this class allows me to add custom pemissions to the shared_with field in sagas, on top of checking membership"
    "Allows me to get shared files for one user or filter users w/wo/o their roles for a an saga types "

    class ROLES(models.TextChoices): 
        VIEWER = 'viewer', 'View-only'
        EDITOR = 'editor', 'Can Edit'
        ADMIN = 'admin', "Full Access"
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saga = models.ForeignKey(Saga, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLES.choices, default = ROLES.VIEWER)

    class Meta:
        unique_together = ('user', 'saga')

class Series(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_series')
    title = models.CharField(max_length=255)
    description = models.TextField()
    sagas = models.ManyToManyField(Saga, blank= True, related_name= 'series' )
    shared_with = models.ManyToManyField(User, through='SagaMembership', blank= True)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class SeriesMembership(models.Model):
    class ROLES(models.TextChoices):
        VIEWER = 'viewer', "View-onlky"
        EDITOR = 'editor', "Can Edit"
        ADMIN = 'admin', "Full Access"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLES.choices, default=ROLES.VIEWER)


class Entry(models.Model):
    "Single Table Based Inheritance model allows us to map different story notes to one model in the DB"
    "journal, idea, fundamental"

    class EntryType(models.TextChoices):
        JOURNAL = "J", "Journal"
        IDEA =  "I", "Idea"
        NEWS = "N", "News"
    
    class SessionType(models.TextChoices):
        NY = "NY", "New York"
        TKYO =  "TYO", "Toyo"
        LON = "LON", "London"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_entry')
    entry_type = models.CharField(max_length=20, choices = EntryType.choices, default=EntryType.IDEA)
    shared_with = models.ManyToManyField(User, through='EntryMembership', null= True, blank= True)
    trades = models.ManyToManyField(Trade,  blank = True)
    series = models.ManyToManyField(Series,  blank = True)
    title = models.CharField(max_length=255, default='title')
    comments = models.TextField(null = True, blank=True)

    # Journal
    symbol = models.CharField(max_length=12, default = 'symbol', null = True, blank= True)
    trading_session = models.CharField(choices = SessionType.choices, null = True, blank= True, verbose_name="Trading Session")
    entry_daily = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry Daily")
    entry_4HR = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 4H")
    entry_2H = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 2H")
    entry_1H = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 1H")
    entry_30M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 30M")
    entry_15M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 15M")
    entry_5M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 5M")
    entry_1M = models.CharField(max_length=300, null = True, blank= True, verbose_name="Entry 1M")

    # News
    headline_title = models.CharField(max_length=50, null = True, blank= True, verbose_name= 'Headline Title')
    headline_url = models.CharField(max_length=100, null = True, blank= True, verbose_name= 'Headline Url')
    published_date = models.DateTimeField(verbose_name= 'Publish Date', null= True, blank= True)
    source = models.CharField(max_length=30, null= True, blank= True)
    
    # General
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default= dict, blank=True)

    def __str__(self):
        return f"{self.get_entry_type}  {self.title}"

    @property
    def get_entry_type(self):
        return f'{self.entry_type}'

class EntryMembership(models.Model):
    "this class allows me to set meteadeta and not only test membership of an account that is listed under shared_with"
    "Allows me to get shared files for a user or filter user w/w/o roles "
   
    class ROLES(models.TextChoices):
        VIEWER = 'viewer', "View-only"
        EDITOR = 'editor', "Can Edit"
        ADMIN = 'admin', "Full Access"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices= ROLES.choices, default=ROLES.VIEWER)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            unique_together = ('user', 'entry')




