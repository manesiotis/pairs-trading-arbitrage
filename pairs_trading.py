# Pairs Trading Strategy: KO vs PEP
# Author: Konstantinos Manesiotis

#import libraries

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

os.makedirs("plots", exist_ok=True)

#data

start = "2020-01-01"
end = "2024-12-31"
data = yf.download(['KO', 'PEP'], start=start, end=end, auto_adjust=False)['Adj Close']
data = data[['KO', 'PEP']].dropna()


#cointegration

score, pvalue, _ = sm.tsa.coint(data['KO'], data['PEP'])
print(f"Cointegration p-value: {pvalue:.4f}")

#spread & Z-score

hedge_ratio = sm.OLS(data['KO'], sm.add_constant(data['PEP'])).fit().params['PEP']
spread = data['KO'] - hedge_ratio * data['PEP']
zscore = (spread - spread.mean()) / spread.std()

#spread & Z score plot

plt.figure(figsize=(12, 6))
plt.plot(spread, label='Spread')
plt.axhline(spread.mean(), color='black', linestyle='--')
plt.title("Spread between KO and PEP")
plt.legend()
plt.savefig("plots/spread_chart.png")
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(zscore, label='Z-score')
plt.axhline(1, color='red', linestyle='--')
plt.axhline(-1, color='green', linestyle='--')
plt.title("Z-score of the Spread")
plt.legend()
plt.savefig("plots/zscore_chart.png")
plt.show()

#trading signals

data['Z'] = zscore
data['Position'] = 0
data.loc[data['Z'] > 1, 'Position'] = -1  # Short KO, Long PEP
data.loc[data['Z'] < -1, 'Position'] = 1  # Long KO, Short PEP
data['Position'] = data['Position'].shift(1)

#PnL

returns = data['KO'].pct_change() - hedge_ratio * data['PEP'].pct_change()
strategy_returns = returns * data['Position']
cumulative_returns = (1 + strategy_returns.fillna(0)).cumprod()

plt.figure(figsize=(12, 5))
plt.plot(cumulative_returns, label='Strategy')
plt.title("Cumulative Returns")
plt.legend()
plt.savefig("plots/cumulative_returns_chart.png")
plt.show()

















