
import pandas as pd

def build_composite_score(quality_df, growth_score_df, risk_df):
  
  composite_df = pd.DataFrame(index=quality_df.index)

  composite_df["Quality_Score"] = quality_df["Quality_Score"]
  composite_df["Growth_Score"] = growth_score_df["Growth_Score"]
  composite_df["Risk_Score"] = risk_df["Risk_Score"]

  composite_df["Composite_Score"] = (
      0.45 * composite_df["Quality_Score"] +
      0.35 * composite_df["Growth_Score"] -
      0.20 * composite_df["Risk_Score"]
  )
  
  composite_df["Composite_Score"] = composite_df["Composite_Score"].clip(0, 100)
  composite_df = composite_df.round(2)
  
  return composite_df
