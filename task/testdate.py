from datetime import datetime

from api.models import Status
from data import data


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
    if time.weekday() in [3, 4]:
        # holiday:
        return False
    if time > time.replace(hour=12, minute=30, second=0, microsecond=0):
        # after market
        return False
    if time < time.replace(hour=8, minute=30, second=0, microsecond=0):
        # before market
        return False
    return True

# TODO: move to jalali.py
def jalali_to_timestamp(jalali_date):
    from . import jalali
    jdate = "{}/{}/{}".format(jalali_date[:4], jalali_date[4:6], jalali_date[6:8])
    gorgeain_date = jalali.Persian(jdate).gregorian_string("{}/{}/{}")
    import time
    import datetime
    timestamp = time.mktime(datetime.datetime.strptime(gorgeain_date, "%Y/%m/%d").timetuple())
    date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # print('conveted from {} to timestamp: {} which is equal to {}'.format(jalali_date, timestamp, date))
    return 1000*timestamp
