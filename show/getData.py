import requests as r
import json
from show.models import company

server_url = 'http://66.70.160.142:8000/mabna/api'


def company_data():
    for company_id in range(2, 50):
        print(company_id)
        company_filter = '/stock/companies?id={}'.format(company_id)
        output = r.get(server_url, params={'url': company_filter})
        output = json.loads(output.text)
        data = output['data'][0]
        add_to_db_company(data)



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
        new_company = company(**company_dict).save()
