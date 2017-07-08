from task.dates import Check
from api.models import MarketWatch

keys = {
    'InstrumentName': 'نماد', 'InstrumentTitle': 'نام', 'TotalNumberOfTrades': 'تعداد',
    'TotalNumberOfSharesTraded': 'حجم',
    'TotalTradeValue': 'ارزش معاملات', 'PreviousDayPrice': 'دیروز', 'FirstTradePrice': 'اولین',
    'LastTradePrice': 'آخرین', 'ClosingPrice': 'پایانی',
    'LowestTradePrice': 'کمترین', 'HighestTradePrice': 'بیشترین', 'Eps': 'Eps', 'PricePerEarning': 'P/E',
    'SymbolId': 'symbol_id',
}


def query(query_text):
    # print(Check().last_market())
    date = Check().last_market()
    # query_text = 'LastTradeDate={} and '.format(date) + query_text
    query_text = 'SELECT * FROM api_MarketWatch WHERE {} ORDER BY TotalNumberOfSharesTraded DESC'.format(query_text)
    results = MarketWatch.objects.raw(query_text)
    # query_text = 'select * from api_MarketWatch where {}'.format(query_text)
    # results = MarketWatch.objects.filter(LastTradeDate=Check().last_market()).raw(query_text)
    r = []
    for result in results:
        if result.dict(keys, date) != 'wrong symbol':
            r.append(result.dict(keys, date))
    # r = [ if result.dict(keys, date) != 'wrong symbol' else continue ]
    return {'keys': keys, 'result': r}

# keys = [
#     {'InstrumentName': 'نماد'},{'InstrumentTitle': 'نام'}, {'TotalNumberOfTrades': 'تعداد'},
#     {'TotalNumberOfSharesTraded': 'حجم'},
#     {'TotalTradeValue': 'ارزش معاملات'}, {'PreviousDayPrice': 'دیروز'}, {'FirstTradePrice': 'اولین'},
#     {'LastTradePrice': 'آخرین'}, {'ClosingPrice': 'پایانی'},
#     {'LowestTradePrice': 'کمترین'}, {'HighestTradePrice': 'بیشترین'}, {'Eps': 'Eps'}, {'PricePerEarning': 'P/E'},
#     {'SymbolId': 'symbol_id'},
# ]
