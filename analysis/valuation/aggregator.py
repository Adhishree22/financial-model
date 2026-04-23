
import pandas as pd
import numpy as np

def build_valuation_summary(valuation_df, df, forecast):
  
  valuation_df["Expected_Price_EV_Blended"] = (
      valuation_df["Expected_Price_EV_EBITDA"] * 0.35 +
      valuation_df["Expected_Price_EV_Revenue"] * 0.40 +
      valuation_df["Expected_Price_EV_EBIT"] * 0.25
  ).round(2)

  valuation_df["Blended_Price"] = (
      valuation_df["Expected_Price_PE"] * 0.45 +
      valuation_df["Expected_Price_EV_Blended"] * 0.40 +
      valuation_df["Expected_Price_FCF_Yield"] * 0.15
  ).round(2)

  forward_price = valuation_df["Blended_Price"].reindex(forecast.index)
  
  market_hist = (df["Closing"] * df["Shares"]).round(2)
  market_fore = (forward_price * forecast["Shares"]).round(2)
  
  valuation_df["MarketCap"] = pd.concat([market_hist, market_fore])
  
  return valuation_df
