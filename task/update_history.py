from api.models import MarketWatch, Stock
from datetime import datetime
from data import redis
import requests as r, json

def update_history():
	updated_stocks = get_updated_stocks()
	update_stocks(updated_stocks)
	return 'finish'


def get_updated_stocks():
	symbols = MarketWatch.objects.filter(LastTradeDate=str(datetime.today())[:10]).values('SymbolId')
	symbols_dict = []
	for symbol in symbols:
		SymbolId =  symbol['SymbolId']
		mabna_id = Stock.objects.filter(symbol_id=SymbolId).first().mabna_id
		symbol_dict = {'mabna_id':mabna_id,'SymbolId':SymbolId}
		symbols_dict.append(symbol_dict)
	return symbols_dict


def update_stocks(symbols_dict,step=50):
	historical_data_keys = dict(
    date='date_time',
    close='close_price',
    low='low_price',
    high='high_price',
    open='open_price',
    volume='volume',
    )
	for symbol_dict in symbols_dict:
		data = get_updated_data(symbol_dict['mabna_id'])
		for key in historical_data_keys:
			SymbolId = symbol_dict['SymbolId']
			last = eval(redis.hget(SymbolId,key))
			last.append(data[historical_data_keys[key]])
			redis.hset(SymbolId,key,last)


def get_updated_data(mabna_id):
	url = '/exchange/trades?instrument.id={}&_sort=-date_time&_count=1'.format(mabna_id)
	output = r.get('http://66.70.160.142/mabna/api',params={'url':url}).text
	data = json.loads(output)['data'][0]
	return data

# from task.update_history import update_history as h
