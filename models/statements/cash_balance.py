
import numpy as np
import pandas as pd

def build_cash_balance(df, forecast):
  forecast["ChangeInCash"] = (
      forecast["OperatingCashFlow"]
      + forecast["InvestingCashFlow"]
      + forecast["FinancingCashFlow"]
  )
	
  forecast["FreeCashFlow"] = (
      forecast["OperatingCashFlow"]
      + forecast["Capex"]
  )

  fx_ratio = (df["FX"] / df["OperatingCashFlow"]).replace([np.inf, -np.inf], np.nan).dropna().mean()
  forecast["FX"] = forecast["OperatingCashFlow"] * fx_ratio
  
  opening_cash = df["EndingCash"].iloc[-1]

  cash_list = []
  begin_list = []

  for year in forecast.index:
    
    begin_list.append(opening_cash)

    change_cash = (
        forecast.loc[year, "OperatingCashFlow"]
        + forecast.loc[year, "InvestingCashFlow"]
        + forecast.loc[year, "FinancingCashFlow"]
        + forecast["FX"].loc[year]
    )

    closing_cash = opening_cash + change_cash

    cash_list.append(closing_cash)
    opening_cash = closing_cash

  forecast["BeginningCash"] = begin_list
  forecast["EndingCash"] = cash_list

  return forecast
