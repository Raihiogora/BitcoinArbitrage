#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Cryptocurrency:
    # class variable
    _id_count = 0

    def __init__(self, name='undefined', codelist=list()):
        Cryptocurrency._id_count += 1
        self._id = Cryptocurrency._id_count
        self.__name = name
        self.__codelist = codelist
        #self.__market_value = {} # => 'KRAKEN':{'BTC':15,'EUR':55}
        #self.__withdraw = {}  # => 'KRAKEN':12.0 BTC

    # currency = 'BTC', 'EUR', 'USD'
    #def add_market(self, market_name, currency=None, value=None):
    #    if currency is None or value is None:
    #        return
    #    market = self.__market_value.get(market_name)
    #    if market is None:
    #        self.__market_value[market_name] = {currency: value}
    #    else:
    #        market[currency] = value
    #        # currency_value = market.get(currency)
    #        # if currency_value is None:
    #        #     market[currency]=value

    @property
    def code_list(self):
        return self.__codelist

    @property
    def code(self):
        return self.__codelist[0]

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name.__repr__()


class CryptoManager:
    # global managers
    _manager = None

    @classmethod
    def initialize(cls, currency_manager):
        cls._manager = CryptoManager(currency_manager)

    @classmethod
    def get_manager(cls):
        return cls._manager

    @classmethod
    def get_manager_dict(cls):
        return cls._manager.dict

    def __init__(self, currency_market=None):
        self.__currencyMarket = currency_market
        self._dict = dict()
        self._dict['BTC'] = Cryptocurrency('Bitcoin', ('BTC', 'XBT'))
        self._dict['ETH'] = Cryptocurrency('Ethereum', ('ETH',))
        self._dict['BCH'] = Cryptocurrency('Bitcoin Cash', ('BCH', 'BCC'))
        self._dict['ETC'] = Cryptocurrency('Ethereum Classic', ('ETC',))
        self._dict['XLM'] = Cryptocurrency('Stellar Lumen', ('XLM',))
        self._dict['XRP'] = Cryptocurrency('Ripple', ('XRP',))
        self._dict['LTC'] = Cryptocurrency('Litecoin', ('LTC',))
        self._dict['DASH'] = Cryptocurrency('Dash', ('DASH',))
        self._dict['ZEC'] = Cryptocurrency('ZCash', ('ZEC',))
        self._dict['XMR'] = Cryptocurrency('Monero', ('XMR',))
        self._dict['EOS'] = Cryptocurrency('EOS', ('EOS',))
        self._dict['ICN'] = Cryptocurrency('Iconomi', ('ICN',))
        self._dict['XDG'] = Cryptocurrency('Dogecoin', ('XDG', 'DOGE'))
        self._dict['GNO'] = Cryptocurrency('GNO??', ('GNO',))
        self._dict['REP'] = Cryptocurrency('Augur', ('REP',))
        self._dict['MLN'] = Cryptocurrency('Melon', ('MLN',))
        self._dict['MCO'] = Cryptocurrency('MCO??', ('MCO',))
        self._dict['QTUM'] = Cryptocurrency('QTUM??', ('QTUM',))
        self._dict['OMG'] = Cryptocurrency('OMG??', ('OMG',))
        self._dict['ADA'] = Cryptocurrency('ADA??', ('ADA',))

    @property
    def dict(self):
        return self._dict

    def get_from_code(self, code='XXX'):
        return self._dict[code]


# end of file