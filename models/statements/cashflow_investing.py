
import numpy as np
import pandas as pd

def build_investing_cashflow(df, forecast):
  
  inv_ratio = (df["NetInvestmentPurchaseAndSale"] / df["Revenue"]).dropna().median()
  forecast["NetInvestmentPurchaseAndSale"] = forecast["Revenue"] * inv_ratio
  
  bus_ratio = (df["NetBusinessPurchaseAndSale"] / df["Revenue"]).replace([np.inf, -np.inf], np.nan).dropna().median()
  forecast["NetBusinessPurchaseAndSale"] = forecast["Revenue"] * bus_ratio
  
  other_inv_ratio = (df["NetOtherInvestingChanges"] / df["Revenue"]).replace([np.inf, -np.inf], np.nan).dropna().mean()
  forecast["NetOtherInvestingChanges"] = forecast["Revenue"] * other_inv_ratio

  forecast["InvestingCashFlow"] = (
      forecast["Capex"]
      + forecast["NetInvestmentPurchaseAndSale"]
      + forecast["NetBusinessPurchaseAndSale"]
      + forecast["NetOtherInvestingChanges"]
  )

  return forecast
