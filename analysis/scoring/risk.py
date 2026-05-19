
from .utils import normalize
import pandas as pd
import numpy as np

def build_risk_score(ratios_df, growth_df):

  hist = ratios_df[ratios_df.index <= 2025]
  risk_df = pd.DataFrame(index=ratios_df.index)

  risk_df["Leverage_Risk"] = (
      0.4 * normalize(ratios_df["DebtToEquity"], hist["DebtToEquity"]) +
      0.3 * normalize(ratios_df["DebtToAssets"], hist["DebtToAssets"]) +
      0.3 * normalize(ratios_df["NetDebtToEBITDA"], hist["NetDebtToEBITDA"])
  )

  risk_df["Coverage_Risk"] = normalize(
      1 / ratios_df["InterestCoverage"].replace(0, np.nan),
      1 / hist["InterestCoverage"].replace(0, np.nan)
  )

  risk_df["Liquidity_Risk"] = (
      0.5 * normalize(1 / ratios_df["CurrentRatio"], 1 / hist["CurrentRatio"]) +
      0.5 * normalize(1 / ratios_df["QuickRatio"], 1 / hist["QuickRatio"])
  )

  risk_df["CashStress_Risk"] = normalize(ratios_df["Debt_to_FCF_Years"],hist["Debt_to_FCF_Years"])

  risk_df["CashFlow_Risk"] = normalize(1 - ratios_df["FCF_Conversion"],1 - hist["FCF_Conversion"])

  risk_df["Operating_Risk"] = (
    0.5 * normalize(ratios_df["Cost_Rigidity"], hist["Cost_Rigidity"]) +
    0.5 * normalize(ratios_df["Operating_Leverage"], hist["Operating_Leverage"])
  )
  vol = growth_df["Revenue_Growth%"].rolling(3).std()
  hist_vol = vol.loc[vol.index <= 2025]

  risk_df["Volatility_Risk"] = normalize(vol, hist_vol)
  risk_df["Volatility_Risk"] = risk_df["Volatility_Risk"].fillna(0.1)

  cols = [
      "Leverage_Risk", "Coverage_Risk", "Liquidity_Risk",
      "CashStress_Risk", "CashFlow_Risk",
      "Operating_Risk", "Volatility_Risk"
  ]

  for col in cols:
    risk_df[col] = risk_df[col].clip(0, 1)

  risk_df.replace([np.inf, -np.inf], np.nan, inplace=True)
  risk_df.fillna(risk_df.mean(), inplace=True)
  risk_df["Coverage_Risk"] = risk_df["Coverage_Risk"].replace(0, 0.05)

  risk_df["Risk_Score"] = (
      0.20 * risk_df["Leverage_Risk"] +
      0.15 * risk_df["Coverage_Risk"] +
      0.15 * risk_df["Liquidity_Risk"] +
      0.15 * risk_df["CashStress_Risk"] +
      0.10 * risk_df["CashFlow_Risk"] +
      0.10 * risk_df["Operating_Risk"] +
      0.15 * risk_df["Volatility_Risk"]
  ) * 100

  risk_df["Risk_Score"] = risk_df["Risk_Score"].clip(0, 100)

  risk_df["Safety_Score"] = 100 - risk_df["Risk_Score"]
  risk_df["Safety_Score"] = risk_df["Safety_Score"].clip(0, 100)

  risk_df = risk_df.round(2)

  return risk_df
