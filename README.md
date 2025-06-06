# Pairs Trading Strategy: Coca-Cola (KO) vs Pepsi (PEP)

This project implements a basic **statistical arbitrage strategy** known as **Pairs Trading** using Coca-Cola (KO) and PepsiCo (PEP) stock data. The method identifies opportunities to take advantage of temporary deviations in the relative pricing of two cointegrated stocks.

## 💡 What is Pairs Trading?

Pairs trading is a **market-neutral strategy** that involves:

- Identifying a pair of stocks with **long-term price relationship** (cointegration).
- Monitoring the **spread** (difference) between their prices.
- Entering long/short positions when the spread deviates significantly from the mean.
- Profiting when the spread reverts to the mean.

This project uses **linear regression** to find the hedge ratio, calculates the spread and its z-score, and plots key indicators to analyze trading opportunities.

## 📊 What the script does

- Downloads historical price data for KO and PEP from Yahoo Finance.
- Tests for **cointegration** between the two stocks.
- Calculates the **spread** and **z-score** of the relationship.
- Visualizes the cumulative returns, spread, and z-score.
- Lays the groundwork for a simple rule-based trading strategy (e.g., enter when z-score > 2 or < -2).

## 📁 Project structure

pairs-trading/
├── pairs_trading.py # Main script with all calculations and plots
├── plots/
│ ├── cumulative_returns.png # KO vs PEP prices
│ ├── spread.png # Spread between KO and PEP
│ └── zscore.png # Z-score of the spread
├── requirements.txt # Python dependencies
└── README.md # Project explanation and guide

## ⚙️ How to run

1. Install dependencies:

```bash
pip install -r requirements.txt
python pairs_trading.py

🔎 Output
Cointegration p-value printed in the terminal
Three visualizations saved as PNG files:
cumulative_returns.png: shows KO and PEP adjusted prices
spread.png: shows the calculated spread over time
zscore.png: shows standardized spread to identify trading signals

Example console output:
Cointegration p-value: 0.0321

📚 Concepts used
Linear regression (statsmodels) to estimate hedge ratio
Cointegration test (statsmodels.tsa.coint)
Z-score normalization
Time series visualization (matplotlib)

🧑‍💻 Author
Konstantinos Manesiotis

