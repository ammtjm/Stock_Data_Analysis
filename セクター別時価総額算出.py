# Required Libraries
import pandas as pd
import matplotlib.pyplot as plt


# Upload sp500market_cap.csv from local
market_cap_df = pd.read_csv("sp500stock_marketcap_20231124.csv")

# Upload SP500.csv from local
sp500_df = pd.read_csv("sp500.csv")

# Merge the two dataframes based on the company symbols
merged_df = pd.melt(market_cap_df, id_vars=['Date'], var_name='Symbol', value_name='Market_Cap')
merged_df = pd.merge(merged_df, sp500_df, on='Symbol', how='left')

# Calculate the sector-wise market cap for each date
sector_market_cap = merged_df.groupby(['Date', 'GICS Sector'])['Market_Cap'].sum().reset_index()

# Calculate the total market cap for each date
total_market_cap = merged_df.groupby(['Date'])['Market_Cap'].sum().reset_index()
total_market_cap.rename(columns={'Market_Cap': 'Total_Market_Cap'}, inplace=True)

# Merge the sector-wise and total market caps, and calculate the proportion
final_df = pd.merge(sector_market_cap, total_market_cap, on='Date')
final_df['Proportion'] = final_df['Market_Cap'] / final_df['Total_Market_Cap']

# Pivot the dataframe so that the headers represent the sectors and the rows represent the dates
pivot_df = final_df.pivot(index='Date', columns='GICS Sector', values='Proportion')
pivot_df.reset_index(inplace=True)

# Save the pivoted dataframe to a CSV file
pivot_df.to_csv('pivoted_sector_market_cap_proportion_20231124.csv', index=False)

