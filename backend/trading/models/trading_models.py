from django.db import models
from django.conf import settings
from trading.models.account_models import TradingAccount

User = settings.AUTH_USER_MODEL

class Trade(models.Model):
    "Model that holds the data of individual trades"
    "ManytoOne relationship with Trading account"
    class SentimentChoices(models.TextChoices):
        LONG = "LONG", "Long (BUY)"
        SHORT = "SHORT", "SHORT (Sell)"
    
    class TradeStatusChoices (models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"
        CANCELLED = "CANCELLED", "Cancelled"

        
    account = models.ForeignKey(TradingAccount, on_delete=models.SET_NULL, related_name="trades", null = True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    lots = models.DecimalField(default = 0.00, max_digits=10, decimal_places=2, null = True, blank= True)
    symbol = models.CharField(max_length=10, default='symbol')
    entry_price = models.DecimalField(default=0.00, decimal_places=6, help_text="Price at entry", null = True, blank= True)
    exit_price = models.DecimalField(default=0.00, decimal_places=6, null = True, blank=True, help_text="Price at exit")

    realized_pnl = models.DecimalField(max_digits=18 ,decimal_places=2, null=True, blank=True)
    # will either be calcualted on the UI if user has close/open price or user enter manually and that value is captured
    pips = models.DecimalField(max_digits=7, default=0, decimal_places=3, help_text="pips captured in trade", null = True, blank = True)
    entered_time = models.DateTimeField(verbose_name="Trade start time", null = True, blank=True)
    exited_at = models.DateTimeField(null=True, blank=True, verbose_name="Trade end time", null = True, blank =  True)

    direction = models.CharField(max_length=5, choices = SentimentChoices.choices, null=True, blank= True)
    status = models.CharField(default=TradeStatusChoices.OPEN, choices=TradeStatusChoices.choices)

    def __str__(self):
        return f'{self.symbol}  {self.created_at}'
    
    class Meta:
        verbose_name = "trade"
        verbose_name_plural = "trades"

        ordering = ['created_at', 'symbol', 'account']

        db_table = 'trades'

        constraints = [
            models.UniqueConstraint(
                fields = ['account', 'created_at', 'symbol'],
                name='no_duplicate_trades'
            )
        ]

