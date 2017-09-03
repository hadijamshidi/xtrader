from data.redis import load_history

takeprofit = .3
stoploss = .8


def buy_volume_decrease(index=0, initial=10000000, symbol_id='IRO1KAVR0001'):
    close = load_history(symbol_id)['close']
    high = load_history(symbol_id)['high']
    buy = close[index]
    vol = 1
    vol_sum = vol
    margin = initial
    invest = vol * buy
    margin -= invest
    trades_history = [{'price': buy, 'vol': vol}]
    print('bought at price {} and volume {} at i= {}'.format(buy, vol, index))
    # total_lost = 0
    for i, price in enumerate(close[index + 1:]):
        if price < stoploss * buy:
            vol = calc_vol(trades_history, price)
            buy = price
            invest = vol * buy
            vol_sum += vol
            margin -= invest
            print('bought at price {} and volume {} at i= {}'.format(price, vol, i + index))
            trades_history.append({'price': buy, 'vol': vol})
            if margin < 0:
                print('call margin')
                return {'profit': margin - initial, 'action': 'call margin'}
            continue
        if high[i + index] > (takeprofit + 1) * buy:
            margin += high[i + index] * vol_sum
            print(
                'take profit activated at price {} and your margin is {} at i= {}'.format(high[i + index], margin,
                                                                                        i + index))
            return {'profit': margin - initial, 'action': 'tp'}
    return {'profit': margin - initial, 'action': 'failed'}


def calc_vol(history, price):
    loss = 0
    for h in history:
        loss += h['vol'] * (h['price'] - (1+takeprofit) * price)
    return int(loss / ((takeprofit) * price)) + 1


def test():
    result = {}
    for symbol in ['IRO1KAVR0001', 'IRO1IKCO0001', 'IRO1NAFT0001']:
        result[symbol] = []
        for i in range(100):
            summery = buy_volume_decrease(i, symbol_id=symbol)
            if summery['profit'] < 0:
                result[symbol].append({'i': i, 'margin': summery['profit'], 'action': summery['action']})
    return result
