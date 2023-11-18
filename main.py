import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
from TradingAnalyzer import show_market_trend
from decouple import config




mt5.initialize(path=config('PATH_TO_MT5_EXE_FILE'))
server = config('SERVER')
account =  int(config('ACCOUNT_ID'))
password = config('PASSWORD')
if not mt5.initialize(login=account, password=password, server=server):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
authorized=mt5.login(account, password=password, server=server)

if authorized:
    print(mt5.account_info())
    print("Show account_info()._asdict():")
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))



symbol = 'BTCUSDm'
timeframe = mt5.TIMEFRAME_M15
bars = 100




print(show_market_trend(symbol,timeframe,bars,True))