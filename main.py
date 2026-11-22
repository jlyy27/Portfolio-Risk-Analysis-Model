import numpy as np
import pandas as pd
import matplotlib
import yfinance as yf

# the stocks in portfolio to analyse 
tickers = ['AAPL', 'JPM', 'JNJ', 'XOM', 'WMT']
# download stock data from yfinance
data = yf.download(tickers, period = '5y', auto_adjust=True)

# extract closing prices
prices = data['Close']
# show the first 5 rows
print(prices.head())

# calculate daily returns
returns = prices.pct_change().dropna()
print(returns.head())
