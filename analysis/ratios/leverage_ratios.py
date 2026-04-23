
import numpy as np
import pandas as pd

def add_leverage_ratios(full_df, ratios_df):
  
  equity = full_df['Equity'].replace(0, np.nan)
  assets = full_df['TotalAssets'].replace(0, np.nan)
  ebitda = full_df['EBITDA'].replace(0, np.nan)
  interest = full_df['Interest'].replace(0, np.nan)

  #Core leverage ratios
  ratios_df['DebtToEquity'] = full_df['TotalDebt'] / equity
  ratios_df['DebtToAssets'] = full_df['TotalDebt'] / assets
  ratios_df['DebtToEBITDA'] = full_df['TotalDebt'] / ebitda
  
  #Interest Coverage Ratio
  #Visa genuinely has low interest expense
  ratios_df['InterestCoverage'] = full_df['OperatingIncome'] / interest
  
  # Net leverage
  ratios_df['NetDebtToEBITDA'] = full_df['NetDebt'] / ebitda
  
  #Debt Capacity
  #How much more debt company could take safely
  ratios_df["Debt_Capacity"] = 3 - ratios_df["DebtToEBITDA"]
  
  ratios_df.replace([np.inf, -np.inf], np.nan, inplace=True)
  ratios_df = ratios_df.round(2)
  
  return ratios_df
