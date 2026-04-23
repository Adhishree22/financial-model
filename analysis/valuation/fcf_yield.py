
import numpy as np
import pandas as pd

def run_fcf_yield_valuation(fcf_series, hist_df, forecast, name = "FCF_Yield"):

  historical = pd.DataFrame(index=hist_df.index)
  forecast_df = pd.DataFrame(index=forecast.index)

  w_bear, w_base, w_bull = 0.25, 0.5, 0.25

  scale = 1000000
  market_hist = (hist_df["Closing"] * hist_df["Shares"]).round(2)

  fcf_hist = fcf_series.reindex(hist_df.index)
  fcf_fore = fcf_series.reindex(forecast.index)

  historical[name] = (fcf_hist * scale / market_hist).round(4)

  low = historical[name].rolling(3, min_periods=1).quantile(0.25)
  high = historical[name].rolling(3, min_periods=1).quantile(0.75)

  historical["MC_Low"] = (fcf_hist * scale) / high
  historical["MC_Base"] = market_hist
  historical["MC_High"] = (fcf_hist * scale) / low

  historical["Price_Low"] = historical["MC_Low"] / hist_df["Shares"]
  historical["Price_Base"] = hist_df["Closing"]
  historical["Price_High"] = historical["MC_High"] / hist_df["Shares"]


  start = historical[name].iloc[-1]
  target = historical[name].tail(3).median()

  forecast_df[name] = np.linspace(start * 1.05, target, len(forecast))

  low_f = historical[name].tail(3).quantile(0.25)
  high_f = historical[name].tail(3).quantile(0.75)

  forecast_df["MC_Low"] = (fcf_fore * scale) / high_f
  forecast_df["MC_Base"] = (fcf_fore * scale) / forecast_df[name]
  forecast_df["MC_High"] = (fcf_fore * scale) / low_f

  forecast_df["Price_Low"] = forecast_df["MC_Low"] / forecast["Shares"]
  forecast_df["Price_Base"] = forecast_df["MC_Base"] / forecast["Shares"]
  forecast_df["Price_High"] = forecast_df["MC_High"] / forecast["Shares"]

  # Expected price
  historical["Expected_Price"] = (
      historical["Price_Low"] * w_bear +
      historical["Price_Base"] * w_base +
      historical["Price_High"] * w_bull
  )

  forecast_df["Expected_Price"] = (
      forecast_df["Price_Low"] * w_bear +
      forecast_df["Price_Base"] * w_base +
      forecast_df["Price_High"] * w_bull
  )

  current_price = hist_df["Closing"].iloc[-1]

  historical["Expected_Return_%"] = np.nan
  forecast_df["Expected_Return_%"] = ((forecast_df["Expected_Price"] / current_price - 1) * 100)

  historical["Valuation_Gap_%"] = ((historical["Expected_Price"] / historical["Price_Base"] - 1) * 100)

  forecast_df["Valuation_Gap_%"] = ((forecast_df["Expected_Price"] / forecast_df["Price_Base"] - 1) * 100)

  output = pd.concat([historical, forecast_df]).round(2)

  final = pd.DataFrame(index=output.index)

  final[f"{name}"] = output[name]
  final[f"Expected_Price_{name}"] = output["Expected_Price"]
  final[f"Expected_Return_{name}%"] = output["Expected_Return_%"]
  final[f"Valuation_Gap_{name}%"] = output["Valuation_Gap_%"]

  return final
