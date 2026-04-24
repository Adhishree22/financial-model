
from .utils import normalize_scaled
import pandas as pd
import numpy as np

def build_growth_score(growth_df):
  
  hist = growth_df[growth_df.index <= 2025]
  growth_score_df = pd.DataFrame(index=growth_df.index)

  growth_score_df["Revenue_Growth_Score"] = normalize_scaled(growth_df["Revenue_Growth%"], hist["Revenue_Growth%"])
  growth_score_df["Earnings_Growth_Score"] = normalize_scaled(growth_df["NetIncome_Growth%"], hist["NetIncome_Growth%"])
  growth_score_df["CashFlow_Growth_Score"] = normalize_scaled(growth_df["FreeCashFlow_Growth%"], hist["FreeCashFlow_Growth%"])
  growth_score_df["Operating_Growth_Score"] = normalize_scaled(growth_df["OperatingIncome_Growth%"], hist["OperatingIncome_Growth%"])

  reinv = (growth_df["Revenue_Growth%"] - growth_df["TotalAssets_Growth%"]).rolling(2).mean()
  hist_reinv = (hist["Revenue_Growth%"] - hist["TotalAssets_Growth%"]).rolling(2).mean()

  growth_score_df["Reinvestment_Score"] = normalize_scaled(reinv, hist_reinv)
  
  growth_score_df.replace([np.inf, -np.inf], np.nan, inplace=True)

  cols = [
      "Revenue_Growth_Score",
      "Earnings_Growth_Score",
      "CashFlow_Growth_Score",
      "Operating_Growth_Score",
      "Reinvestment_Score"
  ]

  for col in cols:
    growth_score_df[col] = growth_score_df[col].rolling(2).mean()

  growth_score_df.fillna(growth_score_df.mean(), inplace=True)

  growth_score_df["Growth_Score"] = (
      0.25 * growth_score_df["Revenue_Growth_Score"] +
      0.25 * growth_score_df["Earnings_Growth_Score"] +
      0.20 * growth_score_df["CashFlow_Growth_Score"] +
      0.15 * growth_score_df["Operating_Growth_Score"] +
      0.15 * growth_score_df["Reinvestment_Score"]
  ) * 100

  growth_score_df["Growth_Score"] = growth_score_df["Growth_Score"].clip(0, 100)
  growth_score_df= growth_score_df.round(2)
  
  return growth_score_df
