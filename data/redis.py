import redis

from task import testdate, dates

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def set(name, value):
    return r.set(name=name, value=value)


def get(name):
    return r.get(name=name).decode()


def hset(name, key, value):
    return r.hset(name=name, key=key, value=value)


def hget(name, key):
    return r.hget(name=name, key=key).decode()


def delete(names):
    return r.delete(*names)


def keys():
    return r.keys()


def load_history(name):
    needed_keys = ['date', 'open', 'high', 'low', 'close', 'volume']
    data_dict = dict()
    for key in needed_keys:
        data_dict[key] = eval(r.hget(name=name, key=key))
    # date = [dates.to_timestamp(day, mode='mabna') for day in data_dict['date']]
    # data_dict['date'] = date
    return data_dict


def flushall():
    return r.flushall()
