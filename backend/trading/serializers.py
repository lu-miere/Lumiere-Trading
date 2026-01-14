from rest_framework import serializers
from trading.models.trading_models import Trade
from trading.models.account_models import AccountMetrics, TradingAccount
from .models.journal_models import Entry, Series, Saga


class TradeSerializer(serializers.ModelSerializer):
    trading_account_user = serializers.ReadOnlyField(source ='account.user.email')
    trading_account_name = serializers.ReadOnlyField( source = 'account.account_name')
    
    class Meta:
        model = Trade
        fields = ['id', 'created_at', 'updated_at','trading_account_user', 'trading_account_name', 'account', 
                            'lots', 'symbol', 'entry_price', 'exit_price', 'realized_pnl', 'pips',  'direction',  'status']

        read_only_fields = ['id', 'created_at', 'updated_at','trading_account_user', 'trading_account_name', 'account', 
                            'lots', 'symbol', 'entry_price', 'exit_price', 'realized_pnl', 'pips',  'direction',  'status']


class TradeDetailSerializer(serializers.ModelSerializer):
    trading_account_user = serializers.ReadOnlyField(source ='account.user.email')
    trading_account_name = serializers.ReadOnlyField( source = 'account.account_name')

    class Meta:
        model = Trade
        fields = [ 'trading_account_name', 'lots', 'symbol', 'entry_price', 'exit_price',
                'realized_pnl', 'pips', 'entered_time', 'exited_time', 'direction',  'status']

        read_only_fields = ['id', 'trading_account_user', 'account', 'created_at', 'updated_at']

    def validate (self, data):
        instance = self.instance

        entered_time = data.get('entered_time') or getattr(instance, 'entered_time', None)
        exited_time = data.get('exited_time') or getattr(instance, 'exited_time', None)
        status = data.get('status') or getattr(instance, 'status', None)
        exit_price = data.get('exit_price') or getattr(instance, 'exit_price', None)
        errors = {}

        if entered_time and exited_time:
            if entered_time > exited_time:
                errors['exited_time'] =  'Entered time cannot be later than exited time.'
        
        if status == "CLOSED" :
          if exit_price is None or exit_price == 0:
                errors['exit_price']= 'A closed trade must have an exit price.'
          if not exited_time:
                errors['exited_time']= 'A closed trade must have an exit time.'
        else:
            if exited_time:
                errors['exited_time']= 'A trade that is not closed can not have an exit time.'
                
        if errors:
            raise serializers.ValidationError(errors)
        
        return data


                 
class AccountMetricsSerializer(serializers.ModelSerializer):
    trading_account_name = serializers.ReadOnlyField(source = 'account.account_name')

    class Meta:
        model = AccountMetrics 
        fields = [
            'id', 'trading_account_name', 'account_id', 'total_realized_pnl', 'win_rate', 
            'total_trades', 'winning_trades', 'losing_trades', 'breakeven_trades', 
            'avg_win', 'avg_loss', 'lots_traded', 'sharpe_ratio', 'profit_factor',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'account_id', 'created_at', 'updated_at']



class TradingAccountSerializer(serializers.ModelSerializer):
    metrics = AccountMetricsSerializer(read_only = True)
    user_email = serializers.ReadOnlyField(source = 'user.email')
    
    class Meta:
        model = TradingAccount
        fields = ['id', 'account_name', 'user_email', 'initial_deposit', 'equity', 'balance']

        read_only_fields = ['id',  'account_name', 'user_email', 'initial_deposit', 'equity', 'balance' ]


class TradingAccountDetailSerializer(serializers.ModelSerializer):
    metrics = AccountMetricsSerializer(read_only = True)
    user_email = serializers.ReadOnlyField(source = 'user.email')

    class Meta:
        model = TradingAccount
        fields = ['id',  'account_name', 'user_email', 'initial_deposit', 'equity', 'balance', 'metrics' ]

        read_only_fields = ['id',  'account_name', 'user_email', 'initial_deposit', 'equity', 'balance', 'metrics' ]

    def validate_initial_deposit(self, value):
        if self.instance and self.instance.trades.exists():
            if value != self.instance.initial_deposit:
                raise serializers.ValidationError('initial_deposit: Cannot alter initial deposit')
        return value
            

# class SagaSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Saga
#         fields = ['user', 'title', 'created_at', 'updated_at']

#         read_only_fields = ['user', 'title', 'created_at', 'updated_at']

# class SagaDetailSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Saga
#         fields = '__all__'

#         read_only_fields = ['id', 'user']

class SeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = ['id', 'user', 'sagas', 'created_at', 'updated_at']

        read_only_fields = ['id', 'user', 'sagas', 'created_at', 'updated_at']

class SeriesDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Series
        fields = '__all__'
        read_only_fields = ['id', 'user', 'sagas', 'created_at', 'updated_at']

class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ['id', 'user', 'entry_type', 'created_at', 'updated_at', 'trades', 'series', 'title', 
                            'symbol', 'trading_session', 'headline_title',  'source']
        

        read_only_fields = ['id', 'user', 'entry_type', 'created_at', 'updated_at', 'trades', 'series', 'title', 
                            'symbol', 'trading_session', 'headline_title',  'source']
        

class EntryDetailSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = Entry
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at' ]