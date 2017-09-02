from data.redis import load_history

symbol_id = 'IRO1IKCO0001'
takeprofit = .2
stoploss = .9


def buy_volume_decrease(index=0):
    close = load_history(symbol_id)['close']
    buy = close[index]
    vol = 1
    margin = 1000
    invest = vol * buy
    # total_lost = 0
    for price in close[index + 1:]:
        if price < stoploss * buy:
            vol = calc_vol(invest, price, vol)
            buy = price
            invest = vol * buy
        if price > (takeprofit+1)*buy:
            print('yes')


def calc_vol(buy, price, vol):
    loss = (price - buy)*vol
    new_vol = 1
    while (new_vol * takeprofit * price) - loss <= 1:
        new_vol += 1
    return new_vol
