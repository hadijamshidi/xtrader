from .models import Strategy, Follower
from django.contrib.auth.models import User


def add_strategy_to_db(data,userName):
    strategy = dict(
        name=data['name'],
        filters=str(data['filters']),
        watch_list=str(data['stock_names'])
    )
    st = Strategy(**strategy)
    st.save()
    user = User.objects.get_by_natural_key(username=userName)
    Follower(owner=user, strategy=st, follower=user)
    # print(strategy)
    # print(len(strategy['filters']))
    # pass
