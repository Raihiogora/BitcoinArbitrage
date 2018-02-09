#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Currency:
    id_count = 0

    def __init__(self, name='undefined', codelist=()):
        Currency.id_count += 1
        self.__identity = Currency.id_count
        self.__name = name
        self.__codelist = codelist

    @property
    def code_list(self):
        return self.__codelist

    @property
    def code(self):
        return self.__codelist[0]

    def __repr__(self):
        return self.__name.__repr__()


class CurrencyManager:
    # global managers
    _manager = None

    @classmethod
    def initialize(cls):
        cls._manager = CurrencyManager()

    @classmethod
    def get_manager(cls):
        return cls._manager

    @classmethod
    def get_manager_dict(cls):
        return cls._manager.dict

    def __init__(self):
        self._dict = dict()
        self._dict['BTC'] = Currency('Bitcoin', ('BTC', 'XBT'))
        self._dict['ETH'] = Currency('Ethereum', ('ETH',))
        self._dict['EUR'] = Currency('Euro', ('EUR',))
        self._dict['USD'] = Currency('USD', ('USD',))

    @property
    def dict(self):
        return self._dict

    def get_from_code(self, code='XXX'):
        return self._dict[code]


# end of file
