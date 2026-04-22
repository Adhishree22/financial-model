
import numpy as np
import pandas as pd

def compute_growth_rates(full_df):
  
  pct_change_df = full_df.pct_change(fill_method=None) * 100
  pct_change_df.replace([np.inf, -np.inf], np.nan, inplace=True)

  growth_cols = [
      "Revenue", "OperatingIncome", "NetIncome", "EPS",
      "EBITDA", "FreeCashFlow", "PaymentVolume",
      "Transactions", "OperatingExpense", "Dividends", "Shares",
      "OperatingCashFlow", "Capex",
      "TotalAssets", "TotalLiabilities", "Equity"
  ]

  growth_df = pct_change_df[growth_cols].round(5)
  growth_df.columns = [f"{col}_Growth%" for col in growth_df.columns]

  return growth_df


def summarize_growth(growth_df):
  
  summary = pd.DataFrame({
      "Mean": growth_df.mean(),
      "Median": growth_df.median(),
      "StdDev": growth_df.std(),
      "Min": growth_df.min(),
      "Max": growth_df.max()
      }).round(4)

  return summary
