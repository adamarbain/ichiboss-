import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from typing import Dict
import math
import ichiboss_utils

fees = 0.0006

BTC = pd.read_csv('btc_data.csv')
BTC.Date = pd.to_datetime(BTC.Date)

BTC_2022 = BTC[BTC.Date.dt.year == 2022].reset_index(drop=True)

sns.set(style="darkgrid")

# Create the line plot
plt.figure(figsize=(12, 6))
sns.lineplot(x=BTC_2022.Date, y=BTC_2022.Close)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('BTC Price Over Time')

# Rotate dates for readability if needed
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
#plt.show()

netflow = pd.read_csv('netflow.csv')
netflow.Date = pd.to_datetime(netflow.Date, unit='ms').dt.date
netflow.Date = pd.to_datetime(netflow.Date)
#netflow.dtypes
netflow_2022 = netflow[netflow.Date.dt.year == 2022].reset_index(drop=True)
netflow_2022.drop_duplicates()

data = BTC_2022.merge(netflow_2022.NetflowVolume, left_index=True, right_index=True)

data['price_change'] = data.Close.pct_change()

ib = ichiboss_utils.Ichiboss
data['z_score'] = ib.z_score(data.NetflowVolume, 14)

position_data = ib.generate_position(data, 1)

calc_data, sharp_ratio, trade_per_interval, MDD = ib.calc_metrics(position_data, fees, 14)

print(f"Sharp Ratio: {sharp_ratio}\nTrade per Interval: {trade_per_interval}\nMDD: {MDD}")

sns.set(style="darkgrid")

# Create figure and primary axis
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot BTC Price (Left Y-axis)
color = 'tab:blue'
sns.lineplot(x=BTC_2022.Date, y=BTC_2022.Close, ax=ax1, color=color, label='BTC Price')
ax1.set_xlabel('Date')
ax1.set_ylabel('BTC Price (USD)', color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Create secondary axis for Equity
ax2 = ax1.twinx()
color = 'tab:red'
sns.lineplot(x=calc_data.Date, y=calc_data.equity, ax=ax2, color=color, label='Strategy Equity')
ax2.set_ylabel('Equity (Scaled)', color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Add title and format
plt.title('BTC Price vs. Strategy Performance (2020)')
fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.9))

# Rotate dates and adjust layout
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()