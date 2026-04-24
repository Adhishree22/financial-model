
import numpy as np
import pandas as pd

def build_valuation_summary(results_df, df, valuation_df):
  
  dcf_price = results_df.loc["Base", "Price"]
  bear_price = results_df.loc["Low", "Price"]
  bull_price = results_df.loc["High", "Price"]

  current_price = df["Closing"].iloc[-1]
  blended_price = valuation_df["Blended_Price"].iloc[-1]

  weighted_dcf_price = (
      0.2 * bear_price +
      0.6 * dcf_price +
      0.2 * bull_price
  )

  target_price = (
      0.5 * weighted_dcf_price +
      0.3 * blended_price +
      0.2 * current_price
  )

  summary = pd.DataFrame(index=["Valuation"])

  summary["DCF_Price"] = dcf_price
  summary["Market_Price"] = current_price
  summary["Blended_Price"] = blended_price

  summary["Upside_DCF%"] = (dcf_price / current_price - 1) * 100
  summary["Upside_Blended%"] = (blended_price / current_price - 1) * 100
  summary["DCF_vs_Blended_%"] = (dcf_price / blended_price - 1) * 100
                                 
  summary["Weighted_DCF_Price"] = weighted_dcf_price
  summary["Upside_Weighted_DCF%"] = (weighted_dcf_price / current_price - 1) * 100

  summary["Target_Price"] = target_price
  summary["Upside_Target%"] = (target_price / current_price - 1) * 100

  summary = summary.round(2).T
  return summary.round(2).T
