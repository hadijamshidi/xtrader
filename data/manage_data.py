# import requests as r
# from data.models import StockWatch
# from xtrader.localsetting import farabi_login_data
# from data.stockwatch import stockWatchInfo
#
# server_url = 'http://66.70.160.142:8000/mabna/api'
#
# wrong_symbol_ids = []
#
#
# def update_StockWatch(num=0):
#     user = r.session()
#     user.post('http://api.farabixo.com/api/account/repo/login', data=farabi_login_data)
#     stocks = StockWatch.objects.all()
#     for i, stock in enumerate(stocks):
#         if i >= num:
#             print('updating {}-th stockwatch'.format(i))
#             info = stockWatchInfo(stock.SymbolId)
#             if info:
#                 update(stock, info)
#
#
# def update(model, info):
#     for key in info:
#         model.__setattr__(key, info[key])
#     try:
#         model.save()
#         print('successfully updated')
#     except Exception:
#         wrong_symbol_ids.append(dict(id=model.SymbolId, problem='stock watch on update'))
