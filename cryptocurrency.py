#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Cryptocurrency:
    def __init__(self, name = 'undefined', id = 'undefined'):
        self.name = name
        self.id = id
        self.market_value = {} # => 'KRAKEN':{'BTC':15,'EUR':55}
        self.withdraw = {}  # => 'KRAKEN':12.0 BTC

    # currency = 'BTC', 'EUR', 'USD'
    def add_market(self, market_name, currency=None, value=None):
        if currency is None or value is None:
            return
        market = self.market_value.get(market_name)
        if market is None:
            self.market_value[market_name] = {currency: value}
        else:
            market[currency] = value
            # currency_value = market.get(currency)
            # if currency_value is None:
            #     market[currency]=value

    def __str__(self):
        return self.market_value

    def __repr__(self):
        return self.market_value.__repr__()


# end of file