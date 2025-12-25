import math
from django.db.models import Sum, Avg, Count, Q
from django.db.models.functions import TruncDate
from .models.account_models import AccountMetrics
from datetime import date, timedelta
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.db.models.functions import Coalesce
from decimal import Decimal

def recalculate_metrics(account):
        """calculates trade metrics for a trading account, every time a trade is saved
           UPdates the account metrics model and trading account balance
        """
        trades = account.trades.all()
        if not trades.exists():
            metrics, _ = AccountMetrics.objects.get_or_create(account=account)
            metrics.total_realized_pnl =  0
            metrics.total_trades =  0
            metrics.avg_win =   0
            metrics.avg_loss =  0
            metrics.lots_traded = 0
            metrics.winning_trades = 0
            metrics.losing_trades = 0
            metrics.breakeven_trades = 0

        stats =  trades.aggregate(
            total_pnl = Coalesce(Sum('realized_pnl'), Decimal('0.00')),
            count  = Count('id'),
            avg_win = Coalesce(Avg('realized_pnl', filter = Q(realized_pnl__gt = 0)), Decimal('0.00')),
            avg_loss = Coalesce(Avg('realized_pnl', filter= Q(realized_pnl__lt = 0)), Decimal('0.00')),
            total_lots = Coalesce(Sum('lots'), 0),
            sum_wins = Coalesce(Sum('realized_pnl', filter = Q(realized_pnl__gt = 0)), Decimal('0.00')),
            sum_losses = Coalesce(Sum('realized_pnl', filter = Q(realized_pnl__lt = 0)), Decimal('0.00')),
            winning_trades = Count('id', filter = Q(realized_pnl__gt=0)),
            losing_trades = Count('id', filter = Q(realized_pnl__lt=0)),
            breakeven_trades = Count('id', filter = Q(realized_pnl = 0)),
        )

        metrics, _ = AccountMetrics.objects.get_or_create(account=account)
        metrics.total_realized_pnl = stats['total_pnl'] 
        metrics.total_trades = stats['count'] 
        metrics.avg_win =  stats['avg_win'] 
        metrics.avg_loss = stats['avg_loss'] 
        metrics.lots_traded = stats['total_lots'] 
        metrics.winning_trades = stats['winning_trades']
        metrics.losing_trades = stats['losing_trades']
        metrics.breakeven_trades = stats['breakeven_trades']

        if metrics.total_trades > 0:
            metrics.win_rate = (stats['winning_trades']/metrics.total_trades) * 100
        else:
             metrics.win_rate = 0

        if metrics.losing_trades > 0:
            if stats['sum_losses'] != 0:
                metrics.profit_factor = abs(float(stats['sum_wins'])/float(stats['sum_losses']))
            else:
                 metrics.profit_factor = float(abs(stats['sum_wins']))
                 
        metrics.save()

        account.balance = float(account.initial_deposit) + float(metrics.total_realized_pnl)
        account.save()

def get_calendar_trades(account, start, end):
    if start and end:
        trades = account.trades.filter(created_at__range = (start, end))
        
    else:
         start = date.today() - timedelta(days=31 )
         end = date.today()
         trades = account.trades.filter(created_at_range = (start, end))
    
    return (
        trades.annotate(date=TruncDate('created_at')) # Converts Timestamp to Date
        .values('date') # SQL: GROUP BY date
        .annotate(
            trade_count=Count('id'), # Number of trades per day
            daily_pnl=Sum('realized_pnl') # Sum of PnL per day
        )
        .order_by('date')
    )
