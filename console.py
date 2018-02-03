#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = '1.0.0'


"""
https://wiki.python.org/moin/CmdModule
https://pymotw.com/3/cmd/
https://coderwall.com/p/w78iva/give-your-python-program-a-shell-with-the-cmd-module
http://code.activestate.com/recipes/280500-console-built-with-cmd-object/
"""

import os
from datetime import datetime

# from functools import reduce
# import json

def current_time():
    """Current time in string
    Description
    Args:
        None
        #param1 (int): The first parameter.
        #param2 (str): The second parameter.
    Returns:
        string: time in tring format
    """
    return datetime.now().strftime('%H:%M:%S %d-%m-%Y')


def message_start():
    print('start')


def message_end():
    print('end')


if __name__ == '__main__':
    # Clear the screen.
    # os.system('clear')
    message_start()
    print(current_time())
    print('What is your orders ?')
    txt = input('>')
    message_end()
    exit(0)

# end of file
