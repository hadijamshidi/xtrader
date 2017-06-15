from .models import Strategy
from api.models import Stock
from django.contrib.auth.models import User


def add_strategy_to_db(data, user_name):
    strategy = dict(
        trader=User.objects.get_by_natural_key(username=user_name),
        name=data['name'],
        filters=str(data['filters']),
        watch_list=str(data['stock_names'])
    )
    st = Strategy.objects.filter(trader=strategy['trader'], name=strategy['name'])
    st.update(**strategy) if st.exists() else st.create(**strategy)


def load_strategy_names(user_name):
    trader = User.objects.get_by_natural_key(username=user_name)
    names = Strategy.objects.filter(trader=trader).values('name')
    names = [name['name'] for name in names]
    return names


def load_strategy_from_db(user_name,strategy_name):
    trader = User.objects.get_by_natural_key(username=user_name)
    strategy = Strategy.objects.get(trader=trader, name=strategy_name)
    filters, symbol_ids = strategy.filters, strategy.watch_list
    watch_list_dicts_list = get_watch_list_dicts_list(symbol_ids)
    return {'filters': eval(filters), 'stock_names': watch_list_dicts_list}


def get_watch_list_dicts_list(symbol_ids):
    symbol_ids = eval(symbol_ids)
    return [Stock.objects.get(symbol_id=symbol_id).as_json() for symbol_id in symbol_ids]
