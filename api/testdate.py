from datetime import datetime
from api import data
from api.models import Status


def update_MarketWatch():
    times = [i for i in range(0, 60, 5)]
    attr = 'minute'
    condition = True
    counter = 0
    status = Status.objects.get(job='server')
    status.number_of_requests += 1
    status.save()
    while condition:
        if datetime.now().__getattribute__(attr) in times:
            counter = times.index(datetime.now().__getattribute__(attr))
            condition = False
            print('counter set !')

    while status.permision():
        time = datetime.now()
        if time.__getattribute__(attr) in times and validate_time(time):
            if counter == times.index(time.__getattribute__(attr)):
                counter = (counter + 1) % len(times)
                print('updating market watch at {}:{}:{}'.format(datetime.now().hour, datetime.now().minute,
                                                                 datetime.now().second))
                status.market_watch = 'updating'
                status.save()
                data.call_threads_for_marketWatch()
                status.market_watch = 'ready'
                status.save()
                print('finish {}'.format(time))
    status.market_watch = 'ready'
    status.number_of_requests = 0
    status.save()


def validate_time(time):
    ans = True
    if time.weekday() in [3, 4]:
        # holiday:
        ans = False
    if ans and time > time.replace(hour=12, minute=30, second=0, microsecond=0):
        # after market
        ans = False
    if ans and time < time.replace(hour=8, minute=30, second=0, microsecond=0):
        # before market
        ans = False
    return ans
