
import numpy as np
import pandas as pd


def build_efficiency_ratios(full_df, ratios_df):
  
  #Asset Turnover
  ratios_df['AssetTurnover'] = full_df['Revenue'] / full_df['TotalAssets'].replace(0, np.nan)
  
  #Operating Expense Ratio
  ratios_df['OpExRatio'] = full_df['OperatingExpense'] / full_df['Revenue'].replace(0, np.nan)
  
  #Working Capital Turnover
  ratios_df['WorkingCapitalTurnover'] = full_df['Revenue'] / full_df['WorkingCapital'].replace(0, np.nan)
  
  #Operating Leverage
  ratios_df["Operating_Leverage"] = (full_df["OperatingIncome"].pct_change() / full_df["Revenue"].pct_change())
  
  ratios_df.replace([np.inf, -np.inf], np.nan, inplace=True)
  ratios_df = ratios_df.round(2)
  
  return ratios_df
