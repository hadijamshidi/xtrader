import requests as r
import json
from .models import Company, Intradaytrades, Isin
from api.models import Stock

server_url = 'http://66.70.160.142:8000/mabna/api'


def company_data():
    url = '/stock/companies'
    step = 100
    wrongs = []
    for i in range(0, 1400, step):
        print('request for getting Companies from {} until {}'.format(i, i + step))
        output = r.get(server_url, params={'url': url + '?_count=100&_skip={}'.format(i)}).text
        companies = json.loads(output)['data']
        w = add_to_db_company(companies, i)
        wrongs.append(w)

def add_to_db_company(companies, i):
    wrong_ids = []
    for index, company in enumerate(companies):
        data = company
        try:
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
            Company(**company_dict).save()

        except Exception:
            wrong_ids.append(company['id'])
    return wrong_ids

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
    intraday_trades_dict['company'] = Company.objects.get(id=company_id )
    Intradaytrades(**intraday_trades_dict).save()


def clean_duplicate_company():
    companys = Company.objects.all()
    for company in companys:
        check_company = Company.objects.filter(id1=company.id1)
        if len(check_company) > 1:
            remain_company = check_company.first()
            check_company.delete()
            remain_company.save()


def isin_data(start, finish):
    for company_id in range(start, finish):
        company_filter = '/exchange/instruments?stock.company.id={}'.format(company_id)
        output = r.get(server_url, params={'url': company_filter})
        output = json.loads(output.text)
        data = output['data'][0]
        add_to_db_isin(data, company_id)

def add_to_db_isin(data, company_id):
    isin_dict = dict(
        id1=data['id'] if 'id' in data else 0,
        name=data['name'] if 'name' in data else 'False',
        code=data['code'] if 'code' in data else 'False',
        english_name=data['english_name'] if 'english_name' in data else 'False',
        isin=data['isin'] if 'isin' in data else 'False',
        company=Company.objects.get(id1=company_id)
    )
    try:
        Isin(**isin_dict).save()
    except Exception:
        pass
def clean_company():
    clean_duplicate_company()
    companys=Company.objects.filter(exchange='False')
    for company in companys:
        stock=Stock.objects.filter(mabna_short_name=company.trade_symbol)
        stock.delete()
        company.delete()

