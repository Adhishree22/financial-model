
import numpy as np
import pandas as pd

def build_financing_cashflow(df, forecast):
  
  other_fin_ratio = (df["NetOtherFinancingCharges"] / df["TotalDebt"]).mean()
  forecast["NetOtherFinancingCharges"] = forecast["TotalDebt"] * other_fin_ratio

  forecast["FinancingCashFlow"] = (
      forecast["ShareIssued"]
      + forecast["BuyBacks"]
      + forecast["DebtIssued"]
      + forecast["Repayment"]
      + forecast["Dividends"]
      + forecast["NetOtherFinancingCharges"]
  )

  return forecast
