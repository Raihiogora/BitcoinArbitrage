#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

Modules to install
- requests
- xlsxwriter
"""

from currency import CurrencyManager
from cryptocurrency import CryptoManager
from marketplace import MarketManager

# from datetime import datetime
from decimal import *
from functools import reduce
import re
import xlsxwriter

"""
s_crytpo : code of crypto
s_currency : code of currency
c_crypto_curr : list of CryptoInCurrency
"""
def search_crypto_currency(s_crypto, s_currency, l_crypto_curr):
    # recherche si le couple (s_crypto, s_currency) existe pour la place de marché
    s_value = None
    for search in l_crypto_curr:
        if search.crypto.code == s_crypto and search.currency.code == s_currency:
            s_value = search.value
            break
    return s_value


def calculate_compare_markets():
    d_crypto = CryptoManager.get_manager_dict()
    d_market = MarketManager.get_manager_dict()
    d_currency = CurrencyManager.get_manager_dict()
    # l_market = d_market.key()
    # 1) je sélectionne un couple crypt,currency avec le "double for"
    # 2) je crée une matrice associée à ce couple : la matrice prend en X et Y une place de marché
    m_line_markets = list(x for x in d_market.keys())
    for s_crypto, c_crypto in d_crypto.items():
        for s_currency, c_currency in d_currency.items():
            if s_crypto == s_currency:
                break
            # matrix : compare currency between markets
            i_size = len(d_market) # order by l_market
            m_compare_currency = [[None for x in range(i_size)] for y in range(i_size)]
            i_pos_x = 0
            # s_market représente la ligne
            # s_market_compared représente la colonne
            for s_market, c_market in d_market.items():
                # recherche si le couple s_crypto, s_currency existe pour la place de marché
                s_value = search_crypto_currency(s_crypto, s_currency, c_market.cryptoInCurrency.values())
                if s_value is not None:
                    i_pos_y = 0
                    for s_market_compared, c_market_compared in d_market.items():
                        if s_market == s_market_compared:
                            m_compare_currency[i_pos_x][i_pos_y] = Decimal(0)
                        else:
                            # recherche si le couple s_crypto, s_currency existe pour la place de marché
                            s_value_compared = search_crypto_currency(s_crypto, s_currency, c_market_compared.cryptoInCurrency.values())
                            if s_value_compared is not None and Decimal(s_value_compared) > 0.00000001:
                                # Decimal('0.10154500')-Decimal('0.10154500') = Decimal('0E-8') !!
                                # convert in %
                                f_value = Decimal(0.00)
                                if Decimal(s_value) > 0.00000001:
                                    f_value = (Decimal(s_value_compared) - Decimal(s_value)) * Decimal(100.00) / Decimal(s_value)
                                    #if f_value < 0.01 and f_value > -0.01:
                                    #    f_value = None
                                m_compare_currency[i_pos_x][i_pos_y] = f_value
                        i_pos_y += 1
                i_pos_x += 1
            print(s_crypto, s_currency, m_compare_currency)
            c_crypto.add_currency_in_markets_compared(c_currency, m_line_markets, m_compare_currency)


"""
Search for the best in each cryptocurrency
The best is > 1%
"""
def get_best_crypto_conversion():
    l_result = list()
    d_crypto = CryptoManager.get_manager_dict()
    for s_crypto, c_crypto in d_crypto.items():
        for s_currency, item_list in c_crypto.currency_in_markets_compared_dict.items():
            c_currency, markets_compared_matrix = item_list
            i_xpos = 0
            for line in markets_compared_matrix:
                i_ypos = 0
                for column in line:
                    # more than 1%
                    if column is not None and column > 1.00:
                        # we underline it
                        print(s_crypto, s_currency, c_crypto.markets_list[i_xpos], '->', c_crypto.markets_list[i_ypos], column)
                        l_result.append(s_crypto + '-' + s_currency + ' : ' + c_crypto.markets_list[i_xpos] + ' -> ' + c_crypto.markets_list[i_ypos] + ' ' + str(column))
                    i_ypos += 1
                i_xpos += 1
    return l_result


def write_excel_file(matrix, string_list):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('MarketPlaces01.xlsx')
    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    # Iterate over the data and write it out row by row.
    for line in matrix:
        col = 0
        for item in line:
            if re.match('((\d+[\.]\d*$)|(\.)\d+$|\d+$)', item):
                # worksheet.write(row, col, ('%.10f' % item).replace('.', ','))
                worksheet.write(row, col, float(item))
            else:
                worksheet.write(row, col, item)
            col += 1
        row += 1
    # Write a total using a formula.
    # worksheet.write(row, 1, '=SUM(B1:B4)')
    worksheet2 = workbook.add_worksheet()
    row = 0
    for item in string_list:
        worksheet2.write(row, 0, item)
        row += 1
    workbook.close()


if __name__ == '__main__':
    print('start')
    # init main objects
    MarketManager.initialize()
    markets = MarketManager.get_manager()
    markets.load_data()
    # markets.get_market_from_code('KRAKEN').load_data()

    # compare market place for each currency
    calculate_compare_markets()

    # cryptomanager = CryptoManager.get_manager()
    # for key, value in cryptomanager.dictionnary.items():
    #    print(key + ':' + value.__repr__())

    market_position = {'KRAKEN':0,'BINANCE':1,'BITTREX':2,'POLONIEX':3,'GDAX':4}
    currency_position = {'BTC':0,'ETH':1,'EUR':2,'USD':3}
    crypto_position = dict()
    i_count = 1
    for key in CryptoManager.get_manager().dict.keys():
        crypto_position[key] = i_count
        i_count += 1
    # create the matrix
    i_nb_currency = len(currency_position)
    i_nb_market = len(market_position)
    m_values = []
    m_values.extend([['CRYPTO','KRAKEN-BTC','KRAKEN-ETH','KRAKEN-EUR','KRAKEN-USD',
          'BINANCE-BTC','BINANCE-ETH','BINANCE-EUR','BINANCE-USD',
          'BITTREX-BTC','BITTREX-ETH','BITTREX-EUR','BITTREX-USD',
          'POLONIEX-BTC','POLONIEX-ETH','POLONIEX-EUR','POLONIEX-USD',
          'GDAX-BTC','GDAX-ETH','GDAX-EUR','GDAX-USD']])
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

    l_compared = get_best_crypto_conversion()

    write_excel_file(m_values, l_compared)
    # print('\n\n')
    # print('CRYPTO;KRAKEN-BTC;KRAKEN-ETH;KRAKEN-EUR;KRAKEN-USD;'
    #      'BINANCE-BTC;BINANCE-ETH;BINANCE-EUR;BINANCE-USD;'
    #      'BITTREX-BTC;BITTREX-ETH;BITTREX-EUR;BITTREX-USD;'
    #      'POLONIEX-BTC;POLONIEX-ETH;POLONIEX-EUR;POLONIEX-USD;'
    #      'GDAX-BTC;GDAX-ETH;GDAX-EUR;GDAX-USD;'
    #      )
    # print the result table
    # for i in m_values:
    #    print(reduce(lambda x, y: x+';'+y, i))

    print('end')
    exit(0)


# end of file
