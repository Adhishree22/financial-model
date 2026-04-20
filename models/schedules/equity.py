
import numpy as np
import pandas as pd

def build_equity_schedule(df, forecast):
  
  div_payout = (df["Dividends"] / df["NetIncome"]).mean()
  forecast["Dividends"] = forecast["NetIncome"] * div_payout

  buyback_ratio = (df["BuyBacks"] / df["NetIncome"]).median()
  forecast["BuyBacks"] = forecast["NetIncome"] * buyback_ratio

  sbc_ratio = (df["SBC"] / df["Revenue"]).mean()
  forecast["SBC"] = forecast["Revenue"] * sbc_ratio

  issuance_ratio = (df["ShareIssued"] / df["SBC"]).mean()
  forecast["ShareIssued"] = forecast["SBC"] * issuance_ratio
	
	#EquityAdjustment captures residual movements such as OCI, FX translation, and other comprehensive income not explicitly modeled.
  df["EquityAdjustment"] = (df["Equity"].diff() - (df["NetIncome"] + df["Dividends"] + df["ShareIssued"] + df["BuyBacks"] + df["SBC"]))
  eadj_ratio = (df["EquityAdjustment"] / df["Revenue"]).mean()
  forecast["EquityAdjustment"] = forecast["Revenue"] * eadj_ratio

  equity_list = []
  opening_equity = df["Equity"].iloc[-1]

  for year in forecast.index:
    
    closing_equity = (
        opening_equity
        + forecast.loc[year, "NetIncome"]
        + forecast.loc[year, "Dividends"]
        + forecast.loc[year, "BuyBacks"]
        + forecast.loc[year, "ShareIssued"]
        + forecast.loc[year, "SBC"]
        + forecast.loc[year, "EquityAdjustment"]
        )
    
    equity_list.append(closing_equity)
    opening_equity = closing_equity

  forecast["Equity"] = equity_list

  comm_pct = (df["CommonStockEquity"] / df["Equity"]).tail(3).median()
  pref_pct = (df["PreferredStockEquity"] / df["Equity"]).tail(3).median()

  forecast["CommonStockEquity"] = forecast["Equity"] * comm_pct
  forecast["PreferredStockEquity"] = forecast["Equity"] * pref_pct

  return forecast
