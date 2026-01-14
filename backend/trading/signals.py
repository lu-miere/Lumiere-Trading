from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from trading.models.trading_models import Trade,TradingAccount
from authentication.models import User
from trading.models.account_models import AccountMetrics
from .services import recalculate_metrics
from django.apps import AppConfig

# instance is captured thpugh Dependency injection
# basically when django saves to the db, it dispatches a signal 
# django bundles the instance, looks for a list of recievers and broadcasts the instance to them as an arg

@receiver([post_save, post_delete], sender = Trade)
def trigger_trade_metrics_update(sender, instance, **kwargs):

    account = instance.account
    trading_account , created = AccountMetrics.objects.get_or_create(account=account)
    recalculate_metrics(trading_account)

@receiver([post_save], sender = TradingAccount)
def create_metrics_row_for_new_account(sender, instance, created, **kwargs):

    if created:
        AccountMetrics.objects.create(account=instance)

@receiver([post_save], sender = User)
def create_inital_trading_account_upon_register(sender, created, instance, **kwargs):
    if created:
        TradingAccount.objects.create(account = instance)