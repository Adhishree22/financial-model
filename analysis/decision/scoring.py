
import pandas as pd
import numpy as np


def get_recommendation(score):
  if score >= 65:
    return "BUY"
  elif score >= 40:
    return "HOLD"
  else:
    return "SELL"


def get_confidence_label(score):
  if score >= 75:
    return "HIGH CONVICTION"
  elif score >= 55:
    return "MEDIUM CONVICTION"
  else:
    return "LOW CONVICTION"


def upside_to_score(upside):
  return np.clip(upside * 2, 0, 100)


def build_decision(quality_df, growth_df, risk_df, valuation_summary, results_df, df):
  
  base_year=2025
  terminal_year=2030
	
  base_quality = quality_df.loc[base_year, "Quality_Score"]
  base_growth = growth_score_df.loc[base_year, "Growth_Score"]
  base_risk = risk_df.loc[base_year, "Risk_Score"]

  terminal_quality = quality_df.loc[terminal_year, "Quality_Score"]
  terminal_growth_s = growth_score_df.loc[terminal_year, "Growth_Score"]
  terminal_risk = risk_df.loc[terminal_year, "Risk_Score"]

  dcf_price = valuation_summary["DCF_Price"].iloc[0]
  bear_price  = results_df.loc["Low", "Price"]
  bull_price  = results_df.loc["High", "Price"]

  market_price = df["Closing"].iloc[-1]
  blended_price = valuation_summary["Blended_Price"].iloc[0]

  upside_dcf = valuation_summary["Upside_DCF%"].iloc[0]
  upside_blended = valuation_summary["Upside_Blended%"].iloc[0]

  weighted_price = valuation_summary["Weighted_DCF_Price"].iloc[0]
  target_price = valuation_summary["Target_Price"].iloc[0]

  upside_weighted  = valuation_summary["Upside_Weighted_DCF%"].iloc[0]
  upside_target  = valuation_summary["Upside_Target%"].iloc[0]

  quality_score = base_quality
  growth_score   = base_growth
  risk_score     = 100 - base_risk

  quality_momentum = terminal_quality - base_quality
  growth_momentum  = terminal_growth_s - base_growth
  risk_momentum    = base_risk - terminal_risk


  value_score = (
      0.5 * upside_to_score(upside_dcf) +
      0.3 * upside_to_score(upside_blended) +
      0.2 * upside_to_score(upside_weighted)
  )

  business_score = (
      0.4 * quality_score +
      0.3 * growth_score +
      0.3 * risk_score
  )

  momentum_score = np.clip(
      50 +
      0.4 * quality_momentum +
      0.3 * growth_momentum +
      0.3 * risk_momentum,
      0, 100
  )

  final_score = (
      0.45 * value_score +
      0.35 * business_score +
      0.20 * momentum_score
  )

  confidence_score = (
      0.4 * business_score +
      0.3 * momentum_score +
      0.3 * (100 - abs(upside_dcf - upside_blended))
  )


  decision_df = pd.DataFrame(index=["INVESTMENT_THESIS"])

  decision_df["Value_Score"] = value_score
  decision_df["Business_Score"] = business_score
  decision_df["Momentum_Score"] = momentum_score
  decision_df["Final_Score"] = final_score

  decision_df["Recommendation"] = get_recommendation(final_score)
  decision_df["Confidence_Score"] = confidence_score
  decision_df["Confidence"] = get_confidence_label(confidence_score)

  decision_df["DCF_Price"] = dcf_price
  decision_df["Bear_Price"] = bear_price
  decision_df["Bull_Price"] = bull_price
  decision_df["Blended_Price"] = blended_price
  decision_df["Market_Price"] = current_price
  decision_df["Weighted_Price"] = weighted_price
  decision_df["Target_Price"] = target_price

  decision_df["Upside_DCF%"] = upside_dcf
  decision_df["Upside_Blended%"] = upside_blended
  decision_df["Upside_Weighted%"] = upside_weighted
  decision_df["Upside_Target%"] = upside_target

  decision_df["Base_Quality"] = base_quality
  decision_df["Base_Growth"] = base_growth
  decision_df["Base_Risk"] = base_risk

  decision_df["Terminal_Quality"] = terminal_quality
  decision_df["Terminal_Growth"] = terminal_growth
  decision_df["Terminal_Risk"] = terminal_risk
  
  decision_df = decision_df.round(2)
  
  return decision_df
