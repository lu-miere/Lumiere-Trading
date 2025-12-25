from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from trading.models.trading_models import Trade,TradingAccount
from trading.models.account_models import AccountMetrics
from services import recalculate_metrics
from django.apps import AppConfig


@receiver([post_save, post_delete], sender = Trade)
# instance is captured thpugh Dependency injection
# basically when django saves to the db, it dispatches a signal 
# django bundles the instance, looks for a list of recievers and broadcasts the instance to them as an arg
def trigger_trade_metrics_update(sender, instance, **kwargs):

    account = instance.account
    metrics , created = AccountMetrics.objects.get_or_create(account=account)
    recalculate_metrics(metrics)

@receiver([post_save], sender = TradingAccount)
def create_metrics_row_for_new_account(sender, instance, created, **kwargs):

    if created:
        AccountMetrics.objects.create(account=instance)

