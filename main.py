import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

# calculate the historical Value at Risk (VaR)
historical_var_95 = - np.percentile(portfolio_returns,5) # 95% confidence level
historical_var_99 = -np.percentile(portfolio_returns,1) # 99% confidence level

print(f'\nHistorical VaR (95% confidence): {historical_var_95:.4%}')
print(f'Historical VaR (99% confidence): {historical_var_99:.4%}')

# covert the historical Var to dollar amounts
portfolio_value = 10000 # assume a portfolio value of $10000

historical_var_95_dollar = historical_var_95 * portfolio_value
historical_var_99_dollar = historical_var_99 * portfolio_value

print(f'\nHistorical VaR (95% confidence) in dollars: ${historical_var_95_dollar:.2f}')
print(f'Historical VaR (99% confidence) in dollars: ${historical_var_99_dollar:.2f}')

# calculate the parametric VaR
parametric_var_95 = - (portfolio_mean - 1.65 * portfolio_std) # 95% confidence level
parametric_var_99 = - (portfolio_mean - 2.33 * portfolio_std) # 99% confidence level

print(f'\nParametric VaR (95% confidence): {parametric_var_95:.4%}')
print(f'Parametric VaR (99% confidence): {parametric_var_99:.4%}')

# convert the parametric VaR to dollar amounts
parametric_var_95_dollar = parametric_var_95 * portfolio_value
parametric_var_99_dollar = parametric_var_99 * portfolio_value

print(f'\nParametric VaR (95% confidence) in dollars: ${parametric_var_95_dollar:.2f}')
print(f'Parametric VaR (99% confidence) in dollars: ${parametric_var_99_dollar:.2f}')  

# Calculate historical Expected Shortfall (ES)
tail_returns_95 = portfolio_returns[portfolio_returns <= portfolio_returns.quantile(0.05)]

es_95 = -tail_returns_95.mean()
print(f'\nHistorical Expected Shortfall (95% confidence): {es_95:.4%}')

tail_returns_99 = portfolio_returns[portfolio_returns <= portfolio_returns.quantile(0.01)]
es_99 = -tail_returns_99.mean()
print(f'Historical Expected Shortfall (99% confidence): {es_99:.4%}')



# Now Stress Testing the Portfolio
# Scenario 1: Technology Sector Crash (Nov 2026 Tech Sell-off)
tech_shocks = pd.Series({
    'AAPL': -0.06,
    'JPM': -0.02,
    'JNJ': 0.01,
    'XOM': -0.02,
    'WMT': 0.01
})

tech_shock_portfolio_return = tech_shocks.loc[tickers] @ weights
tech_portfolio_pnl = tech_shock_portfolio_return * portfolio_value

print(f'Tech Sell-off Return: {tech_shock_portfolio_return:.2%}')
print(f'Tech Sell-off PnL: ${tech_portfolio_pnl:.2f}')

# Scenario 2: Broad Market Downturn (Global Recession)
market_shocks = pd.Series({
    'AAPL': -0.08,
    'JPM': -0.07,
    'JNJ': -0.03,
    'XOM': -0.06,
    'WMT': -0.02
})

market_shock_portfolio_return = market_shocks.loc[tickers] @ weights
market_portfolio_pnl = market_shock_portfolio_return * portfolio_value

print(f'Market Downturn Return: {market_shock_portfolio_return:.2%}')
print(f'Market Downturn PnL: ${market_portfolio_pnl:.2f}')

# Scenario 3: Interest Rate Hike ( = 100 bpm)
interest_rate_shocks = pd.Series({
    'AAPL': -0.05,
    'JPM': 0.02,
    'JNJ': -0.02,
    'XOM': -0.01,
    'WMT': -0.03
})

rate_shock_portfolio_return = interest_rate_shocks.loc[tickers] @ weights
rate_portfolio_pnl = rate_shock_portfolio_return * portfolio_value

print(f'Interest Rate Hike Return: {rate_shock_portfolio_return:.2%}')
print(f'Interest Rate Hike PnL: ${rate_portfolio_pnl:.2f}')

# VaR Backtesting: split training n testing data
split_index = int(len(portfolio_returns) * 0.8)

train_returns = portfolio_returns.iloc[:split_index]
test_returns = portfolio_returns.iloc[split_index:]

print(f'\nTraining Data Length: {len(train_returns)}')
print(f'Testing Data Length: {len(test_returns)}')

# calculate the historical VaR on training data
train_historical_var_95 = -np.percentile(train_returns, 5)
train_historical_var_99 = -np.percentile(train_returns, 1)

print(f'\nTraining Historical VaR (95% confidence): {train_historical_var_95:.4%}')
print(f'Training Historical VaR (99% confidence): {train_historical_var_99:.4%}')

# count the number of breaches in the testing data
breaches_95 = test_returns < -train_var_95
breaches_99 = test_returns < -train_var_99

print(f"95% VaR Breaches: {breaches_95.sum()}")
print(f"99% VaR Breaches: {breaches_99.sum()}")

# Calculate breach rates
breach_rate_95 = breaches_95.mean()
breach_rate_99 = breaches_99.mean()

# calculate the parametric VaR on training data
train_mean = train_returns.mean()
train_std = train_returns.std()

train_param_var_95 = -(train_mean - 1.645 * train_std)
train_param_var_99 = -(train_mean - 2.326 * train_std)

print(f"Training Parametric 95% VaR: {train_param_var_95:.4%}")
print(f"Training Parametric 99% VaR: {train_param_var_99:.4%}")

# Count parametric VaR breaches
param_breaches_95 = test_returns < -train_param_var_95
param_breaches_99 = test_returns < -train_param_var_99

print(f"Parametric 95% VaR Breaches: {param_breaches_95.sum()}")
print(f"Parametric 99% VaR Breaches: {param_breaches_99.sum()}")

# Calculate parametric VaR breach rates
param_breach_rate_95 = param_breaches_95.mean()
param_breach_rate_99 = param_breaches_99.mean()

print(f"Parametric 95% VaR Breach Rate: {param_breach_rate_95:.2%}")
print(f"Parametric 99% VaR Breach Rate: {param_breach_rate_99:.2%}")

print(f"95% VaR Breach Rate: {breach_rate_95:.2%}")
print(f"99% VaR Breach Rate: {breach_rate_99:.2%}")
