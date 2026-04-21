
import numpy as np
import pandas as pd

def build_eps(df, forecast):
  
  scale = 1000000
  
  price = ((-df["BuyBacks"] * scale) / (-df["Shares"].diff())).replace([np.inf, -np.inf], np.nan).dropna().tail(3).median()
  
  opening_shares = df["Shares"].iloc[-1]
  shares_list = []
  for year in forecast.index:
    
    shares_issued = (forecast.loc[year, "ShareIssued"] * scale) / price
    shares_bought = (forecast.loc[year, "BuyBacks"] * scale) / price
    sbc_issued = shares_bought = (forecast.loc[year, "SBC"] * scale) / price
    
    closing_shares = opening_shares + shares_issued + sbc_issued + shares_bought
    
    shares_list.append(closing_shares)
    opening_shares = closing_shares
    
  forecast["Shares"] = shares_list
  
  pref_ratio = (df["PreferredStockDividend"] / df["NetIncome"]).replace([np.inf, -np.inf], np.nan).dropna().mean()
  forecast["PreferredStockDividend"] = (forecast["NetIncome"] * pref_ratio)
  
  forecast["NetIncomeCommon"] = (forecast["NetIncome"] - forecast["PreferredStockDividend"])
  
  forecast = forecast.round(2)
  
  forecast["EPS"] = (forecast["NetIncomeCommon"] * scale) / forecast["Shares"]
  
  return forecast
