# Portfolio-Risk-Analysis-Model

A Python-based portfolio risk analysis project that evaluates the risk characteristics of an equally weighted equity portfolio using historical market data.

The model implements portfolio volatility, correlation analysis, market beta, Value at Risk (VaR), Expected Shortfall (ES), stress testing and out-of-sample VaR backtesting.

## 1. Project Overview

This project aims to apply quantitative risk management techniques to a hypothetical investment portfolio, examining potential losses under normal and stressed market conditions.

The analysis focuses on three questions:

- How much risk does the portfolio carry?
- How large could potential daily losses be?
- How well do the estimated risk thresholds perform against unseen historical data?

## 2. Portfolio and Data

The portfolio consists of five equally weighted US equities:

| Ticker | Company | Weight |
|---|---|---:|
| AAPL | Apple | 20% |
| JPM | JPMorgan Chase | 20% |
| JNJ | Johnson & Johnson | 20% |
| XOM | Exxon Mobil | 20% |
| WMT | Walmart | 20% |

- **Initial hypothetical portfolio value:** $10,000
- **Data source:** Yahoo Finance (`yfinance`)
- **Historical period:** Approximately five years
- **Frequency:** Daily adjusted closing prices
- **Portfolio construction:** Constant 20% weights for each asset

## 3. Risk Measures

The model implements:

- **Portfolio Volatility:** Measures fluctuations in daily portfolio returns using asset covariances and portfolio weights.
- **Correlation Analysis:** Examines relationships between individual equity returns and potential diversification benefits.
- **Market Beta:** Estimates the sensitivity of individual equities and the overall portfolio to movements in the S&P 500.
- **Historical VaR:** Estimates 95% and 99% daily loss thresholds using historical portfolio returns.
- **Parametric VaR:** Estimates daily loss thresholds under a normal distribution assumption.
- **Expected Shortfall:** Calculates the average loss on days when losses exceed the historical VaR threshold.

## 4. Stress Testing

Three hypothetical scenarios are applied to evaluate portfolio sensitivity to adverse market movements:

1. Technology sector sell-off
2. Broad market downturn
3. Interest rate increase

Each scenario applies assumed asset-level percentage shocks to estimate the corresponding portfolio return and dollar loss.

