
import numpy as np
import pandas as pd

def build_working_capital(df, forecast):
  
  df["CashAdjustment"] = (df["CashAndCashEquivalents"] +df["OtherShortTermInvestments"]) - df["EndingCash"]
  
  total_ratio = ((df["CashAndCashEquivalents"] +df["OtherShortTermInvestments"]) / df["EndingCash"]).replace([np.inf, -np.inf], np.nan).median()
  cash_split = (df["CashAndCashEquivalents"] / (df["CashAndCashEquivalents"] +df["OtherShortTermInvestments"])).replace([np.inf, -np.inf], np.nan).median()
  
  forecast["CashAndCashEquivalents"] = (forecast["EndingCash"] * total_ratio * cash_split)
  forecast["OtherShortTermInvestments"] = (forecast["EndingCash"] * total_ratio * (1 - cash_split))
  
  rec_ratio = (df["Receivables"] / df["Revenue"]).median()
  oca_ratio = (df["OtherCurrentAssets"] / df["Revenue"]).median()
  rc_ratio = (df["RestrictedCash"] / df["Revenue"]).median()

  forecast["Receivables"] = forecast["Revenue"] * rec_ratio
  forecast["RestrictedCash"] = forecast["Revenue"] * rc_ratio
  forecast["OtherCurrentAssets"] = forecast["Revenue"] * oca_ratio

  forecast["CashAdjustment"] = (
      forecast["CashAndCashEquivalents"]
      + forecast["OtherShortTermInvestments"]
      - forecast["EndingCash"]
  )


  forecast["CurrentAssets"] = (
      forecast["EndingCash"]
      + forecast["CashAdjustment"]
      + forecast["Receivables"]
      + forecast["RestrictedCash"]
      + forecast["OtherCurrentAssets"]
  )

  pay_ratio = (df["PayablesAndAccruedExpenses"] / df["Revenue"]).median()
  pen_ratio = (df["Pension"] / df["Revenue"]).median()
  ocl_ratio = (df["OtherCurrentLiabilities"] / df["Revenue"]).median()

  forecast["PayablesAndAccruedExpenses"] = forecast["Revenue"] * pay_ratio
  forecast["Pension"] = forecast["Revenue"] * pen_ratio
  forecast["OtherCurrentLiabilities"] = forecast["Revenue"] * ocl_ratio

  forecast["CurrentLiabilities"] = (
      forecast["ShortTermDebt"]
      + forecast["PayablesAndAccruedExpenses"]
      + forecast["Pension"]
      + forecast["OtherCurrentLiabilities"]
  )


  forecast["WorkingCapital"] = (forecast["CurrentAssets"] - forecast["CurrentLiabilities"])
  
  forecast["NetDebt"] = (forecast["TotalDebt"] - forecast["CashAndCashEquivalents"])

  return forecast
