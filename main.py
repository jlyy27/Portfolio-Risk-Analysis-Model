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

# calculate correlation matrix
correlation_matrix = returns.corr()

print('\nCorrelation Matrix:\n')
print(correlation_matrix.round(3))

# Calculate the beta of each stock in the portfolio with respect to the portfolio
# download the market index data (S&P 500)
market_data = yf.download('^GSPC', period='5y', auto_adjust=True)
market_prices = market_data['Close']
market_prices = market_prices.squeeze()

# calculate daily market returns
market_returns = market_prices.pct_change().dropna()
print(market_returns.head())

#align the market returns with the portfolio returns
aligned_returns = returns.join(market_returns.rename('Market'), how='inner')
print(aligned_returns.head())

# calculate individual stock beta
market_var = aligned_returns['Market'].var()

stock_beta = aligned_returns[tickers].apply(lambda x: x.cov(aligned_returns['Market']) / market_var)
print('\nStock Betas:\n')
print(stock_beta.round(3))

#calulate portfolio beta
portfolio_beta = stock_beta @ weights
print(f'\nPortfolio Beta: {portfolio_beta:.3f}')

# calculate the historical Value at Risk (VaR)
historical_var_95 = np.percentile(portfolio_returns,5) # 95% confidence level
historical_var_99 = np.percentile(portfolio_returns,1) # 99% confidence level

print(f'\nHistorical VaR (95% confidence): {historical_var_95:.4%}')
print(f'Historical VaR (99% confidence): {historical_var_99:.4%}')

# covert the historical Var to dollar amounts
portfolio_value = 10000 # assume a portfolio value of $10000

historical_var_95_dollar = historical_var_95 * portfolio_value
historical_var_99_dollar = historical_var_99 * portfolio_value

print(f'\nHistorical VaR (95% confidence) in dollars: ${historical_var_95_dollar:.2f}')
print(f'Historical VaR (99% confidence) in dollars: ${historical_var_99_dollar:.2f}')
