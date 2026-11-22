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

# define the weightage of each stock in the portfolio
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2]) # equal weightage for baseline

# calculate daily portfolio returns
portfolio_returns = returns@(weights)
print(portfolio_returns.head())

# calculate the mean and standard deviation of daily portfolio returns
portfolio_mean = portfolio_returns.mean()
portfolio_std = portfolio_returns.std()

print(f"Mean Daily Return: {portfolio_mean:.4%}")
print(f"Daily Standard Deviation: {portfolio_std:.4%}")

# calculate the portofolio volatility
# first, calculate the covariance matrix of returns
cov_matrix = returns.cov()
print(cov_matrix)

# calculate portfolio variance
portfolio_variance = weights.T @ cov_matrix @ weights

# calculate portfolio volatility
portfolio_volatility = np.sqrt(portfolio_variance)
print(f"Portfolio Volatility: {portfolio_volatility:.4%}")

# to check for any discrepancies between the two methods of calculating portfolio volatility
print(np.isclose(portfolio_std, portfolio_volatility))
