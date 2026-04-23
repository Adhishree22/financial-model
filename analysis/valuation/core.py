
import numpy as np
import pandas as pd

def run_valuation_scenario(hist_series, driver_series,hist_df, forecast_df, name, equity = True):
  
  historical_ratios = pd.DataFrame(index=hist_df.index)
  forecast_ratios = pd.DataFrame(index=forecast_df.index)
  
  w_bear, w_base, w_bull = 0.25, 0.5, 0.25
  
  scale = 1000000
  
  driver_hist = driver_series.reindex(hist_df.index)
  driver_fore = driver_series.reindex(forecast_df.index)

  def get_bands(series):
    return (
        series.rolling(3, min_periods=1).quantile(0.25),
        series.rolling(3, min_periods=1).median(),
        series.rolling(3, min_periods=1).quantile(0.75)
        )
    
  if equity:
    
    historical_ratios["Multiple"] = hist_series
    low, base, high = get_bands(hist_series)

    historical_ratios["Price_Low"] = driver_hist * low
    historical_ratios["Price_Base"] = hist_df["Closing"]
    historical_ratios["Price_High"] = driver_hist * high

    start = hist_series.iloc[-1]
    target = hist_series.tail(3).median()

    forecast_ratios["Multiple"] = np.linspace(start * 0.95, target, len(forecast_df))

    recent = hist_series.tail(3)
    low_f, base_f, high_f = recent.quantile(0.25), recent.median(), recent.quantile(0.75)

    forecast_ratios["Price_Low"] = driver_fore * low_f
    forecast_ratios["Price_Base"] = driver_fore * forecast_ratios["Multiple"]
    forecast_ratios["Price_High"] = driver_fore * high_f

  else:
    
    historical_ratios["EV"] = hist_series
    historical_ratios["Multiple"] = hist_series / (driver_hist * scale)

    low, base, high = get_bands(historical_ratios["Multiple"])

    historical_ratios["EV_Low"] = (driver_hist * scale) * low
    historical_ratios["EV_Base"] = hist_series
    historical_ratios["EV_High"] = (driver_hist * scale) * high

    net_debt_hist = hist_df["NetDebt"] * scale
    shares_hist = hist_df["Shares"]

    historical_ratios["Equity_Low"] = historical_ratios["EV_Low"] - net_debt_hist
    historical_ratios["Equity_Base"] = historical_ratios["EV_Base"] - net_debt_hist
    historical_ratios["Equity_High"] = historical_ratios["EV_High"] - net_debt_hist
    
    historical_ratios["Price_Low"] = historical_ratios["Equity_Low"] / shares_hist
    historical_ratios["Price_Base"] = hist_df["Closing"]
    historical_ratios["Price_High"] = historical_ratios["Equity_High"] / shares_hist
    
    # Forecast
    start = historical_ratios["Multiple"].iloc[-1]
    target = historical_ratios["Multiple"].tail(3).median()

    forecast_ratios["Multiple"] = np.linspace(start * 0.95, target, len(forecast_df))

    recent = historical_ratios["Multiple"].tail(3)
    low_f, base_f, high_f = recent.quantile(0.25), recent.median(), recent.quantile(0.75)

    forecast_ratios["EV_Low"] = driver_fore * scale * low_f
    forecast_ratios["EV_Base"] = driver_fore * scale * base_f
    forecast_ratios["EV_High"] = driver_fore * scale * high_f

    net_debt_fore = forecast_df["NetDebt"] * scale
    shares_fore = forecast_df["Shares"]

    forecast_ratios["Equity_Low"] = forecast_ratios["EV_Low"] - net_debt_fore
    forecast_ratios["Equity_Base"] = forecast_ratios["EV_Base"] - net_debt_fore
    forecast_ratios["Equity_High"] = forecast_ratios["EV_High"] - net_debt_fore

    forecast_ratios["Price_Low"] = forecast_ratios["Equity_Low"] / shares_fore
    forecast_ratios["Price_Base"] = forecast_ratios["Equity_Base"] / shares_fore
    forecast_ratios["Price_High"] = forecast_ratios["Equity_High"] / shares_fore
    
  historical_ratios["Expected_Price"] = (
      historical_ratios["Price_Low"] * w_bear +
      historical_ratios["Price_Base"] * w_base +
      historical_ratios["Price_High"] * w_bull
  )
    
  forecast_ratios["Expected_Price"] = (
      forecast_ratios["Price_Low"] * w_bear +
      forecast_ratios["Price_Base"] * w_base +
      forecast_ratios["Price_High"] * w_bull
  )

  current_price = hist_df["Closing"].iloc[-1]
  historical_ratios["Expected_Return_%"] = np.nan
  forecast_ratios["Expected_Return_%"] = (forecast_ratios["Expected_Price"] / current_price - 1) * 100

  historical_ratios["Valuation_Gap_%"] = ((historical_ratios["Expected_Price"] / historical_ratios["Price_Base"] - 1) * 100).round(2)
  forecast_ratios["Valuation_Gap_%"] = ((forecast_ratios["Expected_Price"] / forecast_ratios["Price_Base"] - 1) * 100).round(2)

  output = pd.concat([historical_ratios, forecast_ratios]).round(2)
  final = pd.DataFrame(index=output.index)

  final[f"{name}"] = output["Multiple"]
  final[f"Price_Low_{name}"] = output["Price_Low"]
  final[f"Price_Base_{name}"] = output["Price_Base"]
  final[f"Price_High_{name}"] = output["Price_High"]
  final[f"Expected_Price_{name}"] = output["Expected_Price"]
  final[f"Expected_Return_{name}%"] = output["Expected_Return_%"]
  final[f"Valuation_Gap_{name}%"] = output["Valuation_Gap_%"]

  if not equity:
    final[f"EV_Low_{name}"] = output["EV_Low"]
    final[f"EV_Base_{name}"] = output["EV_Base"]
    final[f"EV_High_{name}"] = output["EV_High"]
    final[f"Equity_Low_{name}"] = output["Equity_Low"]
    final[f"Equity_Base_{name}"] = output["Equity_Base"]
    final[f"Equity_High_{name}"] = output["Equity_High"]

  return final
