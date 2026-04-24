
import pandas as pd
import numpy as np
from .utils import normalize

def build_quality_score(ratios_df):
  
  hist = ratios_df[ratios_df.index <= 2025]
  quality_df = pd.DataFrame(index=ratios_df.index)

  quality_df["Profitability_Quality"] = (
      0.25 * normalize(ratios_df["NetProfitMargin"], hist["NetProfitMargin"]) +
      0.25 * normalize(ratios_df["OperatingMargin"], hist["OperatingMargin"]) +
      0.25 * normalize(ratios_df["EBITDAMargin"], hist["EBITDAMargin"]) +
      0.25 * normalize(ratios_df["GrossMargin"], hist["GrossMargin"])
  )

  quality_df["Return_Quality"] = (
      0.6 * normalize(ratios_df["ROE"], hist["ROE"]) +
      0.4 * normalize(ratios_df["ROA"], hist["ROA"])
  )

  quality_df["Cash_Quality"] = (
      0.25 * normalize(ratios_df["FCF_Conversion"], hist["FCF_Conversion"]) +
      0.25 * normalize(ratios_df["OCF_to_NetIncome"], hist["OCF_to_NetIncome"]) +
      0.25 * normalize(ratios_df["FCF_to_EBITDA"], hist["FCF_to_EBITDA"]) +
      0.25 * normalize(ratios_df["Cash_Conversion"], hist["Cash_Conversion"])
  )

  quality_df["Efficiency_Quality"] = (
      0.4 * normalize(ratios_df["AssetTurnover"], hist["AssetTurnover"]) +
      0.3 * normalize(ratios_df["WorkingCapitalTurnover"], hist["WorkingCapitalTurnover"]) +
      0.3 * normalize(1 - ratios_df["OpExRatio"], 1 - hist["OpExRatio"])
  )

  quality_df["BalanceSheet_Quality"] = (
      0.25 * normalize(1 / ratios_df["DebtToEquity"].replace(0, np.nan), 1 / hist["DebtToEquity"].replace(0, np.nan)) +
      0.25 * normalize(1 / ratios_df["DebtToAssets"].replace(0, np.nan), 1 / hist["DebtToAssets"].replace(0, np.nan)) +
      0.25 * normalize(ratios_df["InterestCoverage"], hist["InterestCoverage"]) +
      0.25 * normalize(1 / ratios_df["NetDebtToEBITDA"].replace(0, np.nan), 1 / hist["NetDebtToEBITDA"].replace(0, np.nan))
  )
  
  quality_df.replace([np.inf, -np.inf], np.nan, inplace=True)
  quality_df.fillna(quality_df.mean(), inplace=True)

  quality_df["Quality_Score"] = (
      0.25 * quality_df["Profitability_Quality"] +
      0.20 * quality_df["Return_Quality"] +
      0.20 * quality_df["Cash_Quality"] +
      0.15 * quality_df["Efficiency_Quality"] +
      0.20 * quality_df["BalanceSheet_Quality"]
  ) * 100
  
  quality_df["Quality_Score"] = quality_df["Quality_Score"].clip(0, 100)
  quality_df = quality_df.round(2)
  
  return quality_df
