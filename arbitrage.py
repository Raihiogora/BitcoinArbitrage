#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cryptocurrency import Cryptocurrency
from marketplace import Marketplace

from datetime import datetime
from functools import reduce
import json
import requests


def call_api(url: str, parameter=None):
    """Call API by url and add parameters
    Description
    Args:
        url (str): http url of api
        parameter (dict): list of parameters
    Returns:
        dict: contains output/response of api
    """
    try_counter = 2
    while try_counter > 0:
        response = requests.get(url, params=parameter)
        # For successful API call, response code will be 200 (OK)
        if not response.ok:
            # webservice error
            print('** API call error code ',response.status_code)
            if (response.status_code==522 or response.status_code==520 or response.status_code==504) and multitry>0:
                print('... no response. new try.')
                try_counter -= 1
            else:
                # If response code is not ok (200), print the resulting http error code with description
                response.raise_for_status()
                exit(1)
                # raise Exception('api not available')
                #  This means something went wrong.
                # raise ApiError('GET /tasks/ {}'.format(response.status_code))
        else:
            return json.loads(response.content)
    raise Exception('api not available')

# https://api.kraken.com/0/public/Ticker?pair=LTCEUR,XBTEUR
# https://api.kraken.com/0/public/AssetPairs
# https://api.kraken.com/0/public/Assets
def load_kraken(cryptos_dict):
    market_name = 'KRAKEN'
    # la liste des valeurs possibles est identifiable dans https://api.kraken.com/0/public/AssetPairs
    wallet={'XXRPXXBT': ('XRP', 'BTC'),'XXRPZEUR': ('XRP', 'EUR'), 'XXRPZUSD':('XRP', 'USD'),
            'XXLMXXBT': ('XLM', 'BTC'),
            'XLTCXXBT': ('LTC', 'BTC'), 'XLTCZEUR': ('LTC', 'EUR'), 'XLTCZUSD': ('LTC', 'USD'),
            'BCHEUR': ('BCH', 'EUR'), 'BCHUSD': ('BCH', 'USD'), 'BCHXBT': ('BCH', 'BTC'),
            'DASHEUR': ('DASH', 'EUR'), 'DASHUSD': ('DASH', 'USD'), 'DASHXBT': ('DASH', 'BTC'),
            'EOSETH': ('EOS', 'ETH'), 'EOSXBT': ('EOS', 'BTC'),
            'GNOETH': ('GNO', 'ETH'), 'GNOXBT': ('GNO', 'BTC'),
            'XETCXXBT': ('ETC', 'BTC'), 'XETCZEUR':('ETC','EUR'), 'XETCZUSD':('ETC','USD'),
            'XETHXXBT': ('ETH', 'BTC'), 'XETHZEUR':('ETH','EUR'), 'XETHZUSD':('ETH','USD'),
            'XICNXETH': ('ICN', 'ETH'), 'XICNXXBT':('ICN','BTC'),
            'XMLNXXBT': ('MLN', 'BTC'),
            'XREPXXBT': ('REP', 'BTC'), 'XREPZEUR':('REP','EUR'),
            'XXBTZEUR': ('BTC', 'EUR'), 'XXBTZUSD':('BTC','USD'),
            'XXDGXXBT': ('XDG', 'BTC'),
            'XXMRXXBT': ('XMR', 'BTC'), 'XXMRZEUR':('XMR','EUR'), 'XXMRZUSD':('XMR','USD'),
            'XZECXXBT': ('ZEC', 'BTC'), 'XZECZEUR':('ZEC','EUR'), 'XZECZUSD':('ZEC','USD'),
            }
    cryptolist = reduce(lambda x, y: x + ',' + y, wallet)
    # example: cryptolist= 'XXBTZEUR,BCHEUR,XETHZEUR,XXRPZEUR,DASHEUR,XLTCZEUR'
    parameters = {'pair': cryptolist}
    json_data = call_api('https://api.kraken.com/0/public/Ticker', parameters)
    # fill data
    str_result = 'result'
    str_currentvalue = 'c'
    for key, (cryptocoin, currency) in wallet.items():
        currency_value = float(json_data[str_result][key][str_currentvalue][0])
        cryptocurrency = cryptos_dict.get(cryptocoin)
        if cryptocurrency is None:
            cryptos_dict[cryptocoin] = Cryptocurrency(cryptocoin, cryptocoin)
        cryptos_dict[cryptocoin].add_market(market_name, currency, currency_value)
    pass


# https://api.binance.com/api/v1/exchangeInfo
# https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
# https://support.binance.com/hc/en-us/articles/115000840592-Binance-API-Beta
#
# https://api.binance.com/api/v1/time
# https://api.binance.com/api/v3/ticker/price
# https://api.binance.com/api/v3/ticker/price?symbol=ETHBTC
def load_binance(cryptos_dict):
    market_name = 'BINANCE'
    wallet={'XRPBTC':('XRP','BTC'), 'ETHBTC': ('ETH', 'BTC'), 'LTCBTC': ('LTC', 'BTC'),
            'ZECBTC': ('ZEC', 'BTC'), 'EOSBTC':('EOS','BTC'), 'BCCBTC':('BCH','BTC'), # point à confirmer ? BCH-BCC ?
            'DASHBTC': ('DASH', 'BTC'), 'ETCBTC':('ETC','BTC'), 'ETCBTC':('ETC','BTC'),
            'ICNBTC': ('ICN', 'BTC'),
            # GNO et MLN et REP et XDG non trouvé !
            #'BNBBTC':('BNB','BTC'), 'NEOBTC':('NEO','BTC'),
            'BCCBTC':('BCH','BTC'),
            #'GASBTC': ('GAS', 'BTC'), 'BTCUSDT': ('BTC', 'USD'), 'HSRBTC': ('HSR', 'BTC'),
            'MCOBTC':('MCO','BTC'), #'WTCBTC':('WTC','BTC'), 'LRCBTC':('LRC','BTC'),
            'QTUMBTC':('QTUM','BTC'), 'OMGBTC':('OMG','BTC'),
            'XMRBTC':('XMR','BTC'), 'XLMBTC':('XLM','BTC'), 'ADABTC':('ADA','BTC')
            }
    parameters = None
    response = call_api('https://api.binance.com/api/v3/ticker/price', parameters)
    # fill data
    str_titre = 'symbol'
    str_price = 'price'
    for key, (cryptocoin, currency) in wallet.items():
        for i in response:
            if i[str_titre]==key:
                currency_value = i[str_price]
                cryptocurrency = cryptos_dict.get(cryptocoin)
                if cryptocurrency is None:
                    cryptos_dict[cryptocoin] = Cryptocurrency(cryptocoin, cryptocoin)
                cryptos_dict[cryptocoin].add_market(market_name, currency, float(currency_value))
                break
    pass


# DOC API V1 : https://bittrex.com/home/api
# https://bittrex.com/api/v1.1/public/getcurrencies
# https://bittrex.com/api/v1.1/public/getticker?market=BTC-LTC
# https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-ltc
# https://bittrex.com/api/v1.1/public/getmarketsummaries
def load_bittrex_v2(cryptos_dict):
    market_name = 'BITTREX'
    wallet={'BTC-XRP':('XRP','BTC'), 'ETH-XRP':('XRP','ETH'),
            'BTC-ETH': ('ETH', 'BTC'), 'USDT-ETH': ('ETH', 'USD'),
            'USDT-BTC': ('XBT', 'USD'),
            'BTC-LTC': ('LTC', 'BTC'), 'ETH-LTC': ('LTC', 'ETH'),
            'BTC-ZEC': ('ZEC', 'BTC'), 'ETH-ZEC': ('ZEC', 'ETH'),
            # 'EOSBTC':('EOS', 'BTC'),
            'BTC-BCC':('BCH', 'BTC'), 'ETH-BCC':('BCH', 'ETH'),
            'BTC-DASH': ('DASH', 'BTC'), 'ETH-DASH': ('DASH', 'ETH'),
            'BTC-ETC':('ETC', 'BTC'), 'ETH-ETC':('ETC', 'ETH'),
            'BTC-GNO':('GNO', 'BTC'), 'ETH-GNO':('GNO', 'ETH'),
            'BTC-MLN':('MLN', 'BTC'),
            'BTC-REP':('REP', 'BTC'), 'ETH-REP':('REP', 'ETH'),
            'BTC-DOGE': ('XDG', 'BTC'),
            # ICN Iconomi - non trouvé dans bittrex
            'BTC-MCO': ('MCO', 'BTC'), 'ETH-MCO': ('MCO', 'ETH'),
            'BTC-QTUM': ('QTUM', 'BTC'), 'ETH-QTUM': ('QTUM', 'ETH'),
            'BTC-OMG': ('OMG', 'BTC'), 'ETH-OMG': ('OMG', 'ETH'),
            'BTC-XMR': ('XMR', 'BTC'), 'ETH-XMR': ('XMR', 'ETH'),
            'BTC-XLM': ('XLM', 'BTC'), 'ETH-XLM': ('XLM', 'ETH'),
            'BTC-ADA': ('ADA', 'BTC'), 'ETH-ADA': ('ADA', 'ETH'),
            # 'BNBBTC':('BNB','BTC'), 'NEOBTC':('NEO','BTC'),
            #'GASBTC': ('GAS', 'BTC'), 'BTCUSDT': ('BTC', 'USD'), 'HSRBTC': ('HSR', 'BTC'),
            #'WTCBTC':('WTC','BTC'), 'LRCBTC':('LRC','BTC'),
            }
    parameters = None
    response = call_api('https://bittrex.com/api/v1.1/public/getmarketsummaries', parameters)
    # fill data
    str_result = 'result'
    str_currentvalue = 'c'
    for key, (cryptocoin, currency) in wallet.items():
        cryptolist = response[str_result]
        for tmp_crypto in cryptolist:
            if tmp_crypto['MarketName'] == key:
                currency_value = tmp_crypto['price']
                cryptocurrency = cryptos_dict.get(cryptocoin)
                if cryptocurrency is None:
                    cryptos_dict[cryptocoin] = Cryptocurrency(cryptocoin,cryptocoin)
                cryptos_dict[cryptocoin].add_market(market_name, currency, currency_value)
                break
    pass


# DOC API : https://github.com/thebotguys/golang-bittrex-api/wiki/Bittrex-API-Reference-(Unofficial)
# API V2.0
# info sur une currency : https://bittrex.com/api/v2.0/pub/Currency/GetCurrencyInfo?currencyName=ETH
def load_bittrex(cryptos_dict):
    market_name = 'BITTREX'
    wallet = {'BTC-XRP': ('XRP', 'BTC'), 'ETH-XRP': ('XRP', 'ETH'),
              'BTC-ETH': ('ETH', 'BTC'), 'USDT-ETH': ('ETH', 'USD'),
              # 'USDT-BTC': ('BTC', 'USD'),
              'BTC-LTC': ('LTC', 'BTC'), 'ETH-LTC': ('LTC', 'ETH'),
              'BTC-ZEC': ('ZEC', 'BTC'), 'ETH-ZEC': ('ZEC', 'ETH'),
              # 'EOSBTC':('EOS', 'BTC'),
              'BTC-BCC': ('BCH', 'BTC'), 'ETH-BCC': ('BCH', 'ETH'),
              'BTC-DASH': ('DASH', 'BTC'), 'ETH-DASH': ('DASH', 'ETH'),
              'BTC-ETC': ('ETC', 'BTC'), 'ETH-ETC': ('ETC', 'ETH'),
              'BTC-GNO': ('GNO', 'BTC'), 'ETH-GNO': ('GNO', 'ETH'),
              'BTC-MLN': ('MLN', 'BTC'),
              'BTC-REP': ('REP', 'BTC'), 'ETH-REP': ('REP', 'ETH'),
              'BTC-DOGE': ('XDG', 'BTC'),
              # ICN Iconomi - non trouvé dans bittrex
              'BTC-MCO': ('MCO', 'BTC'), 'ETH-MCO': ('MCO', 'ETH'),
              'BTC-QTUM': ('QTUM', 'BTC'), 'ETH-QTUM': ('QTUM', 'ETH'),
              'BTC-OMG': ('OMG', 'BTC'), 'ETH-OMG': ('OMG', 'ETH'),
              'BTC-XMR': ('XMR', 'BTC'), 'ETH-XMR': ('XMR', 'ETH'),
              'BTC-XLM': ('XLM', 'BTC'), 'ETH-XLM': ('XLM', 'ETH'),
              'BTC-ADA': ('ADA', 'BTC'), 'ETH-ADA': ('ADA', 'ETH'),
              # 'BNBBTC':('BNB','BTC'), 'NEOBTC':('NEO','BTC'),
              # 'GASBTC': ('GAS', 'BTC'), 'BTCUSDT': ('BTC', 'USD'), 'HSRBTC': ('HSR', 'BTC'),
              # 'WTCBTC':('WTC','BTC'), 'LRCBTC':('LRC','BTC'),
              }
    parameters = None
    response = call_api('https://bittrex.com/api/v2.0/pub/markets/GetMarketSummaries', parameters)
    # fill data
    str_result = 'result'
    # str_currentvalue = 'Summary'
    cryptolist = response[str_result]
    for key, (cryptocoin, currency) in wallet.items():
        for market in cryptolist:
            if market['Summary']['MarketName'] == key:
                currency_value = market['Summary']['Last']
                cryptocurrency = cryptos_dict.get(cryptocoin)
                if cryptocurrency is None:
                    cryptos_dict[cryptocoin] = Cryptocurrency(cryptocoin, cryptocoin)
                cryptos_dict[cryptocoin].add_market(market_name, currency, currency_value)
                break
    pass


# https://poloniex.com/support/api/
# https://poloniex.com/public?command=returnTicker
def load_poloniex(cryptos_dict):
    market_name = 'POLONIEX'
    wallet = {'BTC_XRP': ('XRP', 'BTC'), 'ETH_XRP': ('XRP', 'ETH'),
              'BTC_ETH': ('ETH', 'BTC'), #'USDT_ETH': ('ETH', 'USD'),
              # 'USDT_BTC': ('BTC', 'USD'),
              'BTC_LTC': ('LTC', 'BTC'), 'ETH_LTC': ('LTC', 'ETH'),
              'BTC_ZEC': ('ZEC', 'BTC'), 'ETH_ZEC': ('ZEC', 'ETH'),
              # 'EOSBTC':('EOS', 'BTC'),
              'BTC_BCH': ('BCH', 'BTC'), 'ETH_BCH': ('BCH', 'ETH'),
              'BTC_DASH': ('DASH', 'BTC'), 'ETH_DASH': ('DASH', 'ETH'),
              'BTC_ETC': ('ETC', 'BTC'), 'ETH_ETC': ('ETC', 'ETH'),
              'BTC_GNO': ('GNO', 'BTC'), 'ETH_GNO': ('GNO', 'ETH'),
              'BTC_MLN': ('MLN', 'BTC'),
              'BTC_REP': ('REP', 'BTC'), 'ETH_REP': ('REP', 'ETH'),
              'BTC_DOGE': ('XDG', 'BTC'),
              # ICN Iconomi - non trouvé dans bittrex
              'BTC_MCO': ('MCO', 'BTC'), 'ETH_MCO': ('MCO', 'ETH'),
              'BTC_QTUM': ('QTUM', 'BTC'), 'ETH_QTUM': ('QTUM', 'ETH'),
              'BTC_OMG': ('OMG', 'BTC'), 'ETH_OMG': ('OMG', 'ETH'),
              'BTC_XMR': ('XMR', 'BTC'), 'ETH_XMR': ('XMR', 'ETH'),
              'BTC_XLM': ('XLM', 'BTC'), 'ETH_XLM': ('XLM', 'ETH'),
              'BTC_ADA': ('ADA', 'BTC'), 'ETH_ADA': ('ADA', 'ETH'),
              # 'BNBBTC':('BNB','BTC'), 'NEOBTC':('NEO','BTC'),
              # 'GASBTC': ('GAS', 'BTC'), 'BTCUSDT': ('BTC', 'USD'), 'HSRBTC': ('HSR', 'BTC'),
              # 'WTCBTC':('WTC','BTC'), 'LRCBTC':('LRC','BTC'),
              }
    parameters = None
    response = call_api('https://poloniex.com/public?command=returnTicker', parameters)
    # fill data
    str_result = 'result'
    # str_currentvalue = 'Summary'
    cryptolist = response
    for market, (cryptocoin, currency) in wallet.items():
        result = cryptolist.get(market)
        if result is not None:
            currency_value = result['last']
            cryptocurrency = cryptos_dict.get(cryptocoin)
            if cryptocurrency is None:
                cryptos_dict[cryptocoin] = Cryptocurrency(cryptocoin, cryptocoin)
            cryptos_dict[cryptocoin].add_market(market_name, currency, float(currency_value))
    pass


# DOC API : https://docs.gdax.com/#sandbox
# https://api.gdax.com/products
# https://api.gdax.com/products/BCH-USD/ticker
def load_gdax(cryptos_dict):
    market_name = 'GDAX'
    wallet = {'BCH-BTC': ('BCH', 'BTC'), 'BCH-USD': ('BCH', 'USD'), 'BCH-EUR': ('BCH', 'EUR'),
              'BTC-EUR': ('BTC', 'EUR'), 'BTC-USD': ('BTC', 'USD'),
              'ETH-BTC': ('ETH', 'BTC'), 'ETH-USD': ('ETH', 'USD'), 'ETH-EUR': ('ETH', 'EUR'),
              'LTC-BTC': ('LTC', 'BTC'), 'LTC-USD': ('LTC', 'USD'), 'LTC-EUR': ('LTC', 'EUR'),
              }
    #parameters = None
    #response = call_api('https://api.gdax.com/products', parameters)
    for key, (cryptocoin, currency) in wallet.items():
        market = call_api('https://api.gdax.com/products/'+key+'/ticker')
        currency_value = market.get('price')
        cryptocurrency = cryptos_dict.get(cryptocoin)
        if cryptocurrency is None:
            cryptos_dict[cryptocoin] = Cryptocurrency(cryptocoin, cryptocoin)
        cryptos_dict[cryptocoin].add_market(market_name, currency, float(currency_value))
    pass


marketplace_dict = {}
cryptocurrency_dict = {}
currency_dict = {}


def create_marketplace():
    marketplace_dict['KRAKEN'] = Marketplace('KRAKEN')
    marketplace_dict['BINANCE'] = Marketplace('BINANCE')


def create_cryptocurrency():
    cryptocurrency_dict['BTC'] = Cryptocurrency('Bitcoin', ('XBT','BTC'))
    cryptocurrency_dict['ETH'] = Cryptocurrency('Ethereum', ('ETH'))
    cryptocurrency_dict['XLM'] = Cryptocurrency('Stellar Lumen', ('XLM'))
    cryptocurrency_dict['XRP'] = Cryptocurrency('Ripple', ('XRP'))
    cryptocurrency_dict['LTC'] = Cryptocurrency('Litecoin', ('LTC'))
    cryptocurrency_dict['ZEC'] = Cryptocurrency('ZCash', ('ZEC'))
    cryptocurrency_dict['XMR'] = Cryptocurrency('Monero', ('XMR'))
    cryptocurrency_dict['EOS'] = Cryptocurrency('EOS', ('EOS'))
    cryptocurrency_dict['ICN'] = Cryptocurrency('Iconomi', ('ICN'))
    cryptocurrency_dict['XDG'] = Cryptocurrency('Dogecoin', ('XDG','DOGE'))


def create_currency():
    currency_dict['Bitcoin'] = {'KRAKEN':'XBT', 'BINANCE':'BTC'}
    currency_dict['Euro'] = {'KRAKEN':'EUR', 'BINANCE':'EUR'}
    currency_dict['Dollar'] = {'KRAKEN':'USD', 'BINANCE':'USD'}


if __name__ == '__main__':
    print('start')

    create_currency()
    create_marketplace()
    create_cryptocurrency()
    load_kraken(cryptocurrency_dict)
    load_binance(cryptocurrency_dict)
    load_bittrex(cryptocurrency_dict)
    load_poloniex(cryptocurrency_dict)
    #load_gdax(cryptocurrency_dict)

    for key, value in cryptocurrency_dict.items():
        print(key + ':' + value.__repr__())

    print('\n\n')
    print(  'CRYPTO;KRAKEN-BTC;KRAKEN-ETH;KRAKEN-EUR;KRAKEN-USD;'
            'BINANCE-BTC;BINANCE-ETH;BINANCE-EUR;BINANCE-USD;'
            'BITTREX-BTC;BITTREX-ETH;BITTREX-EUR;BITTREX-USD;'
            'POLONIEX-BTC;POLONIEX-ETH;POLONIEX-EUR;POLONIEX-USD;'
            'GDAX-BTC;GDAX-ETH;GDAX-EUR;GDAX-USD;'
            )

    market_position = {'KRAKEN':1,'BINANCE':2,'BITTREX':3,'POLONIEX':4,'GDAX':5}
    currency_position = {'BTC':1,'ETH':2,'EUR':3,'USD':4}
    value_tab = []
    for cryptocurrency, values_in_markets in cryptocurrency_dict.items():
        marketslist = values_in_markets.market_value
        currency_nb = 4
        market_nb = 5
        value_line = ['' for i in range(1+market_nb*currency_nb)]
        value_line[0] = cryptocurrency
        for market, currencies in marketslist.items():
            for currency, value in currencies.items():
                value_line[market_position[market]*currency_position[currency]] = ('%.10f' % value).replace('.', ',')
        value_tab.extend([value_line])
    # print the result table
    for i in value_tab:
        print(reduce(lambda x, y: x+';'+y, i))
    # Action().cmdloop()
    # example : wait 3600
    print('end')
    exit(0)

# end of file