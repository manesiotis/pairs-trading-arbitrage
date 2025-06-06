# Pairs Trading Strategy: KO vs PEP
# Author: Konstantinos Manesiotis

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# --------- Parameters ---------
ticker1 = 'KO'   # Coca-Cola
ticker2 = 'PEP'  # Pepsi
start = '2020-01-01'
end = '2024-12-31'

# --------- Data Collection ---------
data1 = yf.download(ticker1, start=start, end=end)['Adj Close']
data2 = yf.download(ticker2, start=start, end=end)['Adj Close']
prices = pd.DataFrame({ticker1: data1, ticker2: data2}).dropna()

# --------- Cointegration Test ---------
score, pvalue, _ = sm.tsa.stattools.coint(prices[ticker1], prices[ticker2])
print(f"Cointegration test p-value: {pvalue:.4f}")
if pvalue < 0.05:
    print("✅ Cointegrated pair detected.")
else:
    print("⚠️ Not cointegrated.")

# --------- Hedge Ratio and Spread ---------
model = sm.OLS(prices[ticker1], sm.add_constant(prices[ticker2]))
result = model.fit()
hedge_ratio = result.params[1]
spread = prices[ticker1] - hedge_ratio * prices[ticker2]
zscore = (spread - spread.mean()) / spread.std()

prices['Spread'] = spread
prices['Z-score'] = zscore

# --------- Generate Trading Signals ---------
prices['Position'] = 0
prices.loc[prices['Z-score'] > 1, 'Position'] = -1
prices.loc[prices['Z-score'] < -1, 'Position'] = 1
prices['Position'] = prices['Position'].shift(1)

# --------- Strategy Returns ---------
returns1 = prices[ticker1].pct_change()
returns2 = prices[ticker2].pct_change()
spread_returns = returns1 - hedge_ratio * returns2
strategy_returns = prices['Position'] * spread_returns
cumulative_returns = (1 + strategy_returns.fillna(0)).cumprod()

prices['Strategy_Returns'] = strategy_returns
prices['Cumulative_Returns'] = cumulative_returns

# --------- Plot Cumulative Returns ---------
plt.figure(figsize=(12, 5))
plt.plot(cumulative_returns, label='Strategy Cumulative Returns')
plt.title('Pairs Trading Strategy Performance')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.grid(True)
plt.legend()
plt.show()
