import requests as r
import json
from show.models import Company, Intradaytrades, Isin

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
        # for company_id in range(start, finish):
        #     print(company_id)
        #     company_filter = '/stock/companies?id={}'.format(company_id)
        #     output = r.get(server_url, params={'url': company_filter})
        #     output = json.loads(output.text)
        #     try:
        #         data = output['data'][0]
        #         add_to_db_company(data)
        #     except Exception:
        #         print('Oops: That was no valid number:' + str(company_id) + " try again")


def add_to_db_company(companies, i):
    # print(len(companies))
    wrong_ids = []
    for index, company in enumerate(companies):
        print('trying to add company number: {} id:{}'.format(i + index, company['id']))
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
            new_company = Company(**company_dict).save()
            print('added')
            # new_company.save()
        except Exception:
            wrong_ids.append(company['id'])
            print('{} is has some problem'.format(company['id']))
    return wrong_ids
    # if data['trade_symbol'] != '':
    #     company_dict = dict(
    #         id1=data['id'] if 'id' in data else 0,
    #         name=data['name'] if 'name' in data else 'False',
    #         english_name=data['english_name'] if 'english_name' in data else 'False',
    #         short_name=data['short_name'] if 'short_name' in data else 'False',
    #         english_short_name=data['english_short_name'] if 'english_short_name' in data else 'False',
    #         trade_symbol=data['trade_symbol'] if 'trade_symbol' in data else 'False',
    #         english_trade_symbol=data['english_trade_symbol'] if 'english_trade_symbol' in data else 'False',
    #         state=data['state']['id'] if 'state' in data else 'False',
    #         exchange=data['exchange']['id'] if 'exchange' in data else 'False',
    #         categories=data['categories'][0]['id'] if 'categories' in data else 'False',
    #         metaversion=data['meta']['version'] if ('meta' in data and 'version' in data['meta'])else 'False',
    #     )
    #     try:
    #         Company(**company_dict).save()
    #     except Exception:
    #         print('Oops: That was no valid number:dupilcate')
    #


def intraday_trades_data(start, finish):
    company_intraday_filter = '/exchange/intradaytrades?instrument.stock.company.id={},{}&id_op=bw'.format(start,
                                                                                                           finish)
    output = r.get(server_url, params={'url': company_intraday_filter})
    output = json.loads(output.text)
    # TODO: create loop for ids
    # try:
    #     data = output['data'][0]
    #     add_to_db_company_intraday_trades(data, company_id)
    # except Exception:
    #     print('Oops: there is problem at company id: ' + str(company_id))


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


def duplicate():
    for i in range(0, 575):
        a = Company.objects.filter(id1=i)
        if len(a) > 1:
            a = a.order_by('-id')
            b = a.first()
            for j in a:
                j.delete()
            b.save()


def isin_data(start, finish):
    for company_id in range(start, finish):
        print(company_id)
        company_filter = '/exchange/instruments?stock.company.id={}'.format(company_id)
        output = r.get(server_url, params={'url': company_filter})
        output = json.loads(output.text)
        data = output['data'][0]
        add_to_db_isin(data, company_id)
        try:
            print(data)
        except Exception:
            print('Oops: That was no valid number:' + str(company_id) + " try again")


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
        print('Oops: That was no valid number:dupilcate')
