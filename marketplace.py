#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import reduce
import json
import requests

from currency import CurrencyManager
from cryptocurrency import CryptoManager


class Manager:
    @classmethod
    def class_method(cls):
        pass


class Marketplace:
    __id_count = 0

    def __init__(self, name='undefined'):
        Marketplace.__id_count += 1
        self.__identity = Marketplace.__id_count
        self.__name = name
        self.__cryptoInCurrency = dict()


    def call_api(self, url: str, parameter=None):
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
                print('** API call error code ', response.status_code)
                if (
                        response.status_code == 522 or response.status_code == 520 or response.status_code == 504) and multitry > 0:
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

    @property
    def cryptoInCurrency(self):
        return self.__cryptoInCurrency

    def load_data(self):
        raise Exception('load_data() not available')

    def __repr__(self):
        return self.__name.__repr__()


class MarketManager:
    # global managers
    _manager = None

    @classmethod
    def initialize(cls):
        currency_manager = CurrencyManager.initialize()
        crypto_manager = CryptoManager.initialize(currency_manager)
        cls._manager = MarketManager(crypto_manager)

    @classmethod
    def get_manager(cls):
        return cls._manager

    @classmethod
    def get_manager_dict(cls):
        return cls._manager.dict

    #@staticmethod
    #def initialize():
    #    # global managers
    #    _currencies = CurrencyManager()
    #    _cryptos = CryptoManager(_currencies)
    #    _markets = MarketManager(_cryptos)

    def __init__(self, crypto_market=None):
        self.__cryptoMarket = crypto_market
        self._dict = dict()
        self._dict['KRAKEN'] = KrakenMarket()
        self._dict['BINANCE'] = BinanceMarket()
        self._dict['BITTREX'] = BittrexMarket()
        self._dict['POLONIEX'] = PoloniexMarket()
        self._dict['GDAX'] = GdaxMarket()

    @property
    def dict(self):
        return self._dict

    #@dictionnary.setter
    #def dictionnary(self, value):
    #    if value < 0:
    #        self.__dictionnary = 0
    #    elif value > 1000:
    #        self.__dictionnary = 1000
    #    else:
    #        self.__dictionnary = value

    def get_market_from_code(self, code='undefined'):
        return self.dict.get(code)

    def load_data(self):
        for item in self.dict.values():
            item.load_data()


class CryptoInCurrency:
    def __init__(self, code='undefined', crypto_code='crypto', currency_code='currency'):
        self._code = code
        self._crypto = CryptoManager.get_manager().get_from_code(crypto_code)
        self._currency = CurrencyManager.get_manager().get_from_code(currency_code)
        self._value = None

    @property
    def code(self):
        return self._code

    @property
    def crypto(self):
        return self._crypto

    @property
    def currency(self):
        return self._currency

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


class KrakenMarket(Marketplace):
    def __init__(self):
        Marketplace.__init__(self, name='KRAKEN')
        # la liste des valeurs possibles >> https://api.kraken.com/0/public/AssetPairs
        tmp_cryptoInCurrency = {
                'XXRPXXBT': ('XRP', 'BTC'), 'XXRPZEUR': ('XRP', 'EUR'), 'XXRPZUSD': ('XRP', 'USD'),
                'XXLMXXBT': ('XLM', 'BTC'),
                'XLTCXXBT': ('LTC', 'BTC'), 'XLTCZEUR': ('LTC', 'EUR'), 'XLTCZUSD': ('LTC', 'USD'),
                'BCHEUR': ('BCH', 'EUR'), 'BCHUSD': ('BCH', 'USD'), 'BCHXBT': ('BCH', 'BTC'),
                'DASHEUR': ('DASH', 'EUR'), 'DASHUSD': ('DASH', 'USD'), 'DASHXBT': ('DASH', 'BTC'),
                'EOSETH': ('EOS', 'ETH'), 'EOSXBT': ('EOS', 'BTC'),
                'GNOETH': ('GNO', 'ETH'), 'GNOXBT': ('GNO', 'BTC'),
                'XETCXXBT': ('ETC', 'BTC'), 'XETCZEUR': ('ETC', 'EUR'), 'XETCZUSD': ('ETC', 'USD'),
                'XETHXXBT': ('ETH', 'BTC'), 'XETHZEUR': ('ETH', 'EUR'), 'XETHZUSD': ('ETH', 'USD'),
                'XICNXETH': ('ICN', 'ETH'), 'XICNXXBT': ('ICN', 'BTC'),
                'XMLNXXBT': ('MLN', 'BTC'),
                'XREPXXBT': ('REP', 'BTC'), 'XREPZEUR': ('REP', 'EUR'),
                'XXBTZEUR': ('BTC', 'EUR'), 'XXBTZUSD': ('BTC', 'USD'),
                'XXDGXXBT': ('XDG', 'BTC'),
                'XXMRXXBT': ('XMR', 'BTC'), 'XXMRZEUR': ('XMR', 'EUR'), 'XXMRZUSD': ('XMR', 'USD'),
                'XZECXXBT': ('ZEC', 'BTC'), 'XZECZEUR': ('ZEC', 'EUR'), 'XZECZUSD': ('ZEC', 'USD'),
                               }
        for key, values in tmp_cryptoInCurrency.items():
            self.cryptoInCurrency[key] = CryptoInCurrency(key, values[0], values[1])

    """ 
    https://api.kraken.com/0/public/Ticker?pair=LTCEUR,XBTEUR
    https://api.kraken.com/0/public/AssetPairs
    https://api.kraken.com/0/public/Assets
    """
    def load_data(self):
        print('load KRAKEN')
        const_result = 'result'
        const_currentprice = 'c'
        #code_list = map(lambda x: x.code, self.__cryptoInCurrency.values())
        # example of parameter 'pair' : 'XXBTZEUR,BCHEUR,XETHZEUR,XXRPZEUR,DASHEUR,XLTCZEUR'
        parameters = {'pair': reduce(lambda x, y: x + ',' + y,  self.cryptoInCurrency.keys())}
        json_data = self.call_api('https://api.kraken.com/0/public/Ticker', parameters)
        # for cryptoInCurrency in self.__cryptoInCurrency:
        #    cryptoInCurrency.value = float(json_data[str_result][cryptoInCurrency.code][str_currentvalue][0])
        #for code, crypto in self.__cryptoInCurrency.items():
        #    crypto.value = json_data[const_result][code][const_currentprice][0]
        for key, item in json_data[const_result].items():
            crypto = self.cryptoInCurrency.get(key)
            if crypto is not None:
                crypto.value = item[const_currentprice][0] if item[const_currentprice][0] is not None else ''


class BinanceMarket(Marketplace):
    def __init__(self):
        Marketplace.__init__(self, name='BINANCE')
        # la liste des valeurs possibles >> ?
        tmp_cryptoInCurrency = {
                'XRPBTC': ('XRP', 'BTC'), 'ETHBTC': ('ETH', 'BTC'), 'LTCBTC': ('LTC', 'BTC'),
                'ZECBTC': ('ZEC', 'BTC'), 'EOSBTC': ('EOS', 'BTC'), 'BCCBTC': ('BCH', 'BTC'),
                # point à confirmer ? BCH-BCC ?
                'DASHBTC': ('DASH', 'BTC'), 'ETCBTC': ('ETC', 'BTC'), 'ETCBTC': ('ETC', 'BTC'),
                'ICNBTC': ('ICN', 'BTC'),
                # GNO et MLN et REP et XDG non trouvé !
                # 'BNBBTC':('BNB','BTC'), 'NEOBTC':('NEO','BTC'),
                'BCCBTC': ('BCH', 'BTC'),
                # 'GASBTC': ('GAS', 'BTC'), 'BTCUSDT': ('BTC', 'USD'), 'HSRBTC': ('HSR', 'BTC'),
                'MCOBTC': ('MCO', 'BTC'),  # 'WTCBTC':('WTC','BTC'), 'LRCBTC':('LRC','BTC'),
                'QTUMBTC': ('QTUM', 'BTC'), 'OMGBTC': ('OMG', 'BTC'),
                'XMRBTC': ('XMR', 'BTC'), 'XLMBTC': ('XLM', 'BTC'), 'ADABTC': ('ADA', 'BTC')
                                }
        for key, values in tmp_cryptoInCurrency.items():
            self.cryptoInCurrency[key] = CryptoInCurrency(key, values[0], values[1])

    """
    # https://api.binance.com/api/v1/exchangeInfo
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
    # https://support.binance.com/hc/en-us/articles/115000840592-Binance-API-Beta
    #
    # https://api.binance.com/api/v1/time
    # https://api.binance.com/api/v3/ticker/price
    # https://api.binance.com/api/v3/ticker/price?symbol=ETHBTC
    """
    def load_data(self):
        print('load BINANCE')
        json_data = self.call_api('https://api.binance.com/api/v3/ticker/price', None)
        # example: [{"symbol":"ETHBTC","price":"0.10062100"},{"symbol":"LTCBTC","price":"0.01767900"},
        # {"symbol":"BNBBTC","price":"0.00100700"}, ... ]
        const_titre = 'symbol'
        const_price = 'price'
        # example : json_data=[{"symbol":"ETHBTC","price":"0.10120900"},{"symbol":"LTCBTC","price":"0.01764800"},...]
        for item in json_data:
            crypto = self.cryptoInCurrency.get(item[const_titre])
            if crypto is not None:
                crypto.value = item[const_price] if item[const_price] is not None else ''


class BittrexMarket(Marketplace):
    def __init__(self):
        Marketplace.__init__(self, name='BITTREX')
        # la liste des valeurs possibles >> ?
        tmp_cryptoInCurrency = {
                'BTC-XRP': ('XRP', 'BTC'), 'ETH-XRP': ('XRP', 'ETH'),
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
        for key, values in tmp_cryptoInCurrency.items():
            self.cryptoInCurrency[key] = CryptoInCurrency(key, values[0], values[1])


    """
    # DOC API V1 : https://bittrex.com/home/api
    # https://bittrex.com/api/v1.1/public/getcurrencies
    # https://bittrex.com/api/v1.1/public/getticker?market=BTC-LTC
    # https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-ltc
    # https://bittrex.com/api/v1.1/public/getmarketsummaries
    """
    def load_data_old(self):
        #cryptos_dict = dict()
        #market_name = 'BITTREX'
        #wallet = {'BTC-XRP': ('XRP', 'BTC'), 'ETH-XRP': ('XRP', 'ETH'),}
        #response = self.call_api('https://bittrex.com/api/v1.1/public/getmarketsummaries', None)
        #str_result = 'result'
        #str_currentvalue = 'c'
        #for key, (cryptocoin, currency) in wallet.items():
        #    cryptolist = response[str_result]
        #    for tmp_crypto in cryptolist:
        #        if tmp_crypto['MarketName'] == key:
        #            currency_value = tmp_crypto['price']
        #            cryptocurrency = cryptos_dict.get(cryptocoin)
        #            if cryptocurrency is None:
        #                cryptos_dict[cryptocoin] = Cryptocurrency(cryptocoin, cryptocoin)
        #            cryptos_dict[cryptocoin].add_market(market_name, currency, currency_value)
        #            break
        pass

    # DOC API : https://github.com/thebotguys/golang-bittrex-api/wiki/Bittrex-API-Reference-(Unofficial)
    # API V2.0
    # info sur une currency : https://bittrex.com/api/v2.0/pub/Currency/GetCurrencyInfo?currencyName=ETH
    def load_data(self):
        print('load BITTREX')
        json_data = self.call_api('https://bittrex.com/api/v2.0/pub/markets/GetMarketSummaries', None)
        # example : {"success":true,"message":"","result":[{"Market":{"MarketCurrency":"1ST","BaseCurrency":"BTC",
        # "MarketCurrencyLong":"FirstBlood","BaseCurrencyLong":"Bitcoin","MinTradeSize":2.23693629,
        # "MarketName":"BTC-1ST","IsActive":true,"Created":"2017-06-06T01:22:35.727","Notice":null,
        # "IsSponsored":null,"LogoUrl":"https://bittrexblobstorage.blob.core.windows.net/public/5685a7be-1edf-4ba0-a313-b5309bb204f8.png"},
        # "Summary":{"MarketName":"BTC-1ST","High":0.00006850,"Low":0.00006272,"Volume":646866.00407565,
        # "Last":0.00006272,"BaseVolume":41.68906560,"TimeStamp":"2018-02-04T21:48:10.1","Bid":0.00006272,
        # "Ask":0.00006330,"OpenBuyOrders":348,"OpenSellOrders":5613,"PrevDay":0.00006537,
        # "Created":"2017-06-06T01:22:35.727"},"IsVerified":false}, ... ]}
        const_result = 'result'
        const_summary = 'Summary'
        const_marketname = 'MarketName'
        const_last = 'Last'
        for item in json_data[const_result]:
            crypto = self.cryptoInCurrency.get(item[const_summary][const_marketname])
            if crypto is not None:
                crypto.value = '%.9f' % item[const_summary][const_last]


class PoloniexMarket(Marketplace):
    def __init__(self):
        Marketplace.__init__(self, name='POLONIEX')
        # la liste des valeurs possibles >> ?
        tmp_cryptoInCurrency = {
                'BTC_XRP': ('XRP', 'BTC'), 'ETH_XRP': ('XRP', 'ETH'),
                'BTC_ETH': ('ETH', 'BTC'),  # 'USDT_ETH': ('ETH', 'USD'),
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
        for key, values in tmp_cryptoInCurrency.items():
            self.cryptoInCurrency[key] = CryptoInCurrency(key, values[0], values[1])


    """
    # https://poloniex.com/support/api/
    # https://poloniex.com/public?command=returnTicker
    """
    def load_data(self):
        print('load POLONIEX')
        json_data = self.call_api('https://poloniex.com/public?command=returnTicker', None)
        # example: {"BTC_BCN":{"id":7,"last":"0.00000053","lowestAsk":"0.00000053","highestBid":"0.00000052",
        # "percentChange":"-0.05357142","baseVolume":"46.16168610","quoteVolume":"84643330.08571152","isFrozen":"0",
        # "high24hr":"0.00000058","low24hr":"0.00000051"}, ... }
        const_last = 'last'
        for key, item in json_data.items():
            crypto = self.cryptoInCurrency.get(key)
            if crypto is not None:
                crypto.value = item.get(const_last,'')


class GdaxMarket(Marketplace):
    def __init__(self):
        Marketplace.__init__(self, name='GDAX')
        # la liste des valeurs possibles >> ?
        tmp_cryptoInCurrency = {
                'BCH-BTC': ('BCH', 'BTC'), 'BCH-USD': ('BCH', 'USD'), 'BCH-EUR': ('BCH', 'EUR'),
                'BTC-EUR': ('BTC', 'EUR'), 'BTC-USD': ('BTC', 'USD'),
                'ETH-BTC': ('ETH', 'BTC'), 'ETH-USD': ('ETH', 'USD'), 'ETH-EUR': ('ETH', 'EUR'),
                'LTC-BTC': ('LTC', 'BTC'), 'LTC-USD': ('LTC', 'USD'), 'LTC-EUR': ('LTC', 'EUR'),
                               }
        for key, values in tmp_cryptoInCurrency.items():
            self.cryptoInCurrency[key] = CryptoInCurrency(key, values[0], values[1])

    # DOC API : https://docs.gdax.com/#sandbox
    # https://api.gdax.com/products
    # https://api.gdax.com/products/BCH-USD/ticker
    def load_data(self):
        print('load GDAX')
        # parameters = None
        # response = call_api('https://api.gdax.com/products', parameters)
        const_price = 'price'
        for code, crypto in self.cryptoInCurrency.items():
            market = self.call_api('https://api.gdax.com/products/' + code + '/ticker')
            # example : https://api.gdax.com/products/BCH-BTC/ticker
            # {"trade_id":73971,"price":"0.13927000","size":"0.14374969","bid":"0.13927","ask":"0.13928",
            # "volume":"847.77078226","time":"2018-02-04T22:06:41.220000Z"}
            crypto.value = market.get(const_price, '')


# end of file
