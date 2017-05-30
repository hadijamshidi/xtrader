import requests as r
import json
from show.models import company, intradaytrades

server_url = 'http://66.70.160.142:8000/mabna/api'


def company_data(start, finish):
    for company_id in range(start, finish):
        company_filter = '/stock/companies?id={}'.format(company_id)
        output = r.get(server_url, params={'url': company_filter})
        output = json.loads(output.text)
        try:
            data = output['data'][0]
            add_to_db_company(data)
        except Exception:
            print('Oops: That was no valid number:' + str(company_id) + " try again")


def add_to_db_company(data):
    if data['trade_symbol'] != '':
        company_dict = dict(
            id1=data['id'] if 'id' in data else 0,
            name=data['name'] if 'name' in data else 'False',
            english_name=data['english_name'] if 'english_name' in data else 'False',
            short_name=data['short_name'] if 'short_name' in data else 'False',
            english_short_name=data['english_short_name'] if 'english_short_name' in data else 'False',
            trade_symbol=data['trade_symbol'] if 'trade_symbol' in data else 'False',
            english_trade_symbol=data['english_trade_symbol'] if 'english_trade_symbol' in data else 'False',
            state=data['state']['id'] if 'state' in data else 'False',
            exchange=data['exchange']['id'] if 'exchange' in data else 'False',
            categories=data['categories'][0]['id'] if 'categories' in data else 'False',
            metaversion=data['meta']['version'] if ('meta' in data and 'version' in data['meta'])else 'False',
        )
        company(**company_dict).save()


def intraday_trades_data(company_id):
    company_intraday_filter = '/exchange/intradaytrades?instrument.stock.company.id={}'.format(company_id)
    output = r.get(server_url, params={'url': company_intraday_filter})
    output = json.loads(output.text)
    try:
        data = output['data'][0]
        add_to_db_company_intraday_trades(data, company_id)
    except Exception:
        print('Oops: there is problem at company id: ' + str(company_id))


def add_to_db_company_intraday_trades(data, company_id):
    needed_keys = [
        'date_time',
        'open_price',
        'high_price',
        'low_price',
        'close_price',
        'close_price_change',
        'real_close_price',
        'real_close_price_change',
        "buyer_count",
        "trade_count",
        "volume",
        "value",
    ]
    intraday_trades_dict = dict(
        # id1=data['id'] if 'id' in data else 0,
        trade=data['trade']['id'] if 'trade' in data else 0,
        instrument=data['instrument']['id'] if 'instrument' in data else 0,
        metaversion=data['meta']['version'] if ('meta' in data and 'version' in data['meta'])else 'False',
    )
    for key in needed_keys:
        intraday_trades_dict[key] = data[key]
        intradaytrades(**intraday_trades_dict, company=company.objects.get(id=company_id)).save()
