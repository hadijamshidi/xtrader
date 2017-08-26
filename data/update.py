from data.fundamental import Fundamental
from data.stockwatch import update_stock_watch
from data.update_history import update_history_with_farabixo


def update_all_data(self):
    update_stock_watch()
    f = Fundamental()
    for table in ['ratio', 'income', 'balance', 'marketwatch']:
        f.update(table)
    update_history_with_farabixo(update_stock_watch=False)

