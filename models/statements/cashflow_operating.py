
import numpy as np
import pandas as pd

def build_operating_cashflow(df, forecast):
  
  rev_change = forecast["Revenue"].diff()
  rev_change.iloc[0] = forecast["Revenue"].iloc[0] - df["Revenue"].iloc[-1]
  
  wc_ratio = (df["ChangeWC"] / df["Revenue"].diff()).replace([np.inf, -np.inf], np.nan).dropna().median()
  forecast["ChangeWC"] = rev_change * wc_ratio
  
  amort_ratio = (df["AmortizationOfIntangibles"] / df["GoodwillAndOtherIntangibleAssets"]).replace([np.inf, -np.inf], np.nan).dropna().mean()
  
  opening_gw = df["GoodwillAndOtherIntangibleAssets"].iloc[-1]
  
  gw_list = []
  amort_list = []

  for year in forecast.index:
    
    amort = opening_gw * amort_ratio
    closing_gw = opening_gw - amort  # no acquisitions assumed

    amort_list.append(amort)
    gw_list.append(closing_gw)

    opening_gw = closing_gw

  forecast["AmortizationOfIntangibles"] = amort_list
  forecast["GoodwillAndOtherIntangibleAssets"] = gw_list

  dt_ratio = (df["DeferredTax"] / df["Depreciation"]).replace([np.inf, -np.inf], np.nan).dropna().median()
  forecast["DeferredTax"] = forecast["Depreciation"] * dt_ratio
  
  onc_ratio = (df["OtherNonCashItems"] / df["NetIncome"]).replace([np.inf, -np.inf], np.nan).dropna().median()
  forecast["OtherNonCashItems"] = (forecast["NetIncome"] * onc_ratio)
  
  og_ratio = (df["OperatingGainsLosses"] / df["OperatingExpense"]).replace([np.inf, -np.inf], np.nan).dropna().median()
  forecast["OperatingGainsLosses"] = forecast["OperatingExpense"] * og_ratio

  forecast["OperatingCashFlow"] = (
      forecast["NetIncome"]
      + forecast["Depreciation"]
      + forecast["AmortizationOfIntangibles"]
      + forecast["DeferredTax"]
      + forecast["SBC"]
      + forecast["OtherNonCashItems"]
      + forecast["OperatingGainsLosses"]
      + forecast["ChangeWC"]
  )

  return forecast
