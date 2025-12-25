from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class TradingAccount(models.Model):
    """Model for user trading 
    Data here is synthesized to display metrics on dashboard"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_accounts', help_text="associated user for trading account")
    account_name = models.CharField(max_length=50, default="Primary Account")
    equity = models.DecimalField(default=0.00, max_digits=18, decimal_places=2, help_text='Sum of cash balance and floating positions')
    balance = models.DecimalField(default=0.00, decimal_places=2, help_text='Amount of cash that is settled and avaialble w/o factoring open trades')
    initial_deposit = models.DecimalField(default= 0.00, decimal_places=2, max_digits=12)

    created_at = models.DateTimeField(auto_now_add = True )
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Trading Account for {self.user.email} (ID: {self.id})'
    
    class Meta:
        verbose_name = "Trading Account"
        verbose_name_plural = "Trading Accounts"

        ordering = ['user', 'account_name']

        db_table = 'trading_account'


class AccountMetrics(models.Model):
    """the logic behind this model is that everytime a request is sent to the DB regarding a trade whether entry, modification or deletion
    this model should perform operations based on the fields and track the aggregate performance of the account"""

    """ implements signal to service design pattern where the trade (signal) triggers an event, regardless of where the change on 
     a trade is made, whether via API, django admin, or script, ensuring the metrics are always in sync with a user's trades"""

    """Core metrics for equity curve"""

    account = models.OneToOneField(TradingAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True )
    updated_at = models.DateTimeField(auto_now=True)

    total_realized_pnl = models.DecimalField(default=0.00, decimal_places=2, help_text='')
    win_rate = models.FloatField(default=0.0) 
    total_trades = models.IntegerField(default=0, help_text="total number of entries entered by the traders")
    winning_trades = models.IntegerField(default=0, help_text="total number of trades resulting in postive pnl")
    losing_trades = models.IntegerField(default=0, help_text="total number of trades resulting in negative pnl")
    breakeven_trades = models.IntegerField(default=0, help_text= 'total number of trades resulting in a pnl shoft of 0')
    avg_win = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    avg_loss = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    lots_traded = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, help_text='Total number of lots of all entries for associated trader')

    sharpe_ratio = models.DecimalField(default=0.00, decimal_places=4, max_digits=6)
    profit_factor = models.FloatField(default=0.00)
    # max_drawdown = models.DecimalField(default=0.00, decimal_places=2, help_text="tracks the larget peak to trought declines over trading history ")


    def __str__(self):
        return f"Metrics for {self.account.user} for {self.account.account_name}"
    
    

        # Sharp Ratio is the risk adjusted returns. It is a metric measuring hjow much excess returns you get for extra volatility you endure
        # Returns and sharp ratio are not dorrelated. Two portfolios can have the same returns but different shapr ratios.
        #With portfolio with ratios closer to 0, they experience more volatility while the farther from not considering negative inegers the more stable the return curve 
        # or the less volatility the porfolio endures 
        #we can calculate the sharp for individual trades whic can give us insight on the setup used to take those trades
        #we can calculate the sharp for daily returns to evaluate the if the returns curve is stable becuase 
        # the daily returns is essentially a point of data on our returns curve. 
        # The differnce between those points and how often that happens determisn volatiltiy 



        