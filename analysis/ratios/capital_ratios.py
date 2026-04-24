
import numpy as np
import pandas as pd


def build_capital_ratios(full_df, ratios_df, market_cap):
  
  ratios_df["MarketCap"] = market_cap
  
  #% of FCF Returned to Shareholders
  ratios_df["%_of_FCF_Returned"] = ((abs(full_df["BuyBacks"]) + abs(full_df["Dividends"])) / full_df["FreeCashFlow"].replace(0, np.nan)) * 100
  
  ratios_df["Shareholder_Yield"] = ((abs(full_df["BuyBacks"]) + abs(full_df["Dividends"])) * 1000000 / ratios_df["MarketCap"]) * 100
  
  ratios_df["Payout_Ratio"] = ((abs(full_df["Dividends"]) / full_df["NetIncome"].replace(0, np.nan)) * 100).round(2)
  
  ratios_df["FCF_After_Dividends"] = full_df["FreeCashFlow"].replace(0, np.nan) - full_df["Dividends"]
  
  ratios_df["Buyback_to_FCF"] = (abs(full_df["BuyBacks"]) / full_df["FreeCashFlow"].replace(0, np.nan)) * 100
  
  ratios_df["Net_Shareholder_Return"] = ((abs(full_df["BuyBacks"]) - full_df["ShareIssued"]) * 1000000 / ratios_df["MarketCap"]) * 100
  
  ratios_df.replace([np.inf, -np.inf], np.nan, inplace=True)
  ratios_df = ratios_df.round(2)
  
  return ratios_df
