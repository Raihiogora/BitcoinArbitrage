#!/usr/bin/python3
# -*- coding: utf-8 -*-


from currency import CurrencyManager
from cryptocurrency import CryptoManager
from marketplace import MarketManager

# from datetime import datetime
from functools import reduce


if __name__ == '__main__':
    print('start')
    # init main objects
    MarketManager.initialize()
    markets = MarketManager.get_manager()
    markets.load_data()
    # markets.get_market_from_code('KRAKEN').load_data()

    #cryptomanager = CryptoManager.get_manager()
    #for key, value in cryptomanager.dictionnary.items():
    #    print(key + ':' + value.__repr__())
    print('\n\n')
    print('CRYPTO;KRAKEN-BTC;KRAKEN-ETH;KRAKEN-EUR;KRAKEN-USD;'
          'BINANCE-BTC;BINANCE-ETH;BINANCE-EUR;BINANCE-USD;'
          'BITTREX-BTC;BITTREX-ETH;BITTREX-EUR;BITTREX-USD;'
          'POLONIEX-BTC;POLONIEX-ETH;POLONIEX-EUR;POLONIEX-USD;'
          'GDAX-BTC;GDAX-ETH;GDAX-EUR;GDAX-USD;'
          )

    market_position = {'KRAKEN':0,'BINANCE':1,'BITTREX':2,'POLONIEX':3,'GDAX':4}
    currency_position = {'BTC':0,'ETH':1,'EUR':2,'USD':3}
    crypto_position = dict()
    i_count=0
    for key in CryptoManager.get_manager().dict.keys():
        crypto_position[key] = i_count
        i_count += 1
    # create the matrix
    i_nb_currency = len(currency_position)
    i_nb_market = len(market_position)
    m_values = []
    for s_key, i_pos in crypto_position.items():
        l_values = ['' for i in range(1 + i_nb_market * i_nb_currency)]
        l_values[0] = s_key
        m_values.extend([l_values])
    # fill the matrix
    for s_market, market in MarketManager.get_manager().dict.items():
        for cryptoInCurrency in market.cryptoInCurrency.values():
            s_crypto = cryptoInCurrency.crypto.code_list[0]
            s_currency = cryptoInCurrency.currency.code_list[0]
            s_value = cryptoInCurrency.value
            if s_value is not None:
                m_values[crypto_position[s_crypto]][1 + market_position[s_market] * i_nb_currency + currency_position[s_currency]] = s_value

    #for cryptocurrency, values_in_markets in cryptocurrency_dict.items():
    #    marketslist = values_in_markets.market_value
    #    currency_nb = 4
    #    market_nb = 5
    #    value_line = ['' for i in range(1+market_nb*currency_nb)]
    #    value_line[0] = cryptocurrency
    #    for market, currencies in marketslist.items():
    #        for currency, value in currencies.items():
    #            value_line[market_position[market]*currency_position[currency]] = ('%.10f' % value).replace('.', ',')
    #    value_tab.extend([value_line])
    # print the result table
    for i in m_values:
        print(reduce(lambda x, y: x+';'+y, i))
    # Action().cmdloop()
    # example : wait 3600
    print('end')
    exit(0)

# end of file