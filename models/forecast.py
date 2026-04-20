
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_series(series, periods=5):
  
  X = np.arange(len(series)).reshape(-1, 1)
  y = series.values.reshape(-1, 1)

  model = LinearRegression()
  model.fit(X, y)

  future_X = np.arange(len(series), len(series) + periods).reshape(-1, 1)
  pred = model.predict(future_X).flatten()

  last_year = series.index.max()
  future_index = np.arange(last_year + 1, last_year + periods + 1)
  
  forecast_s = pd.Series(pred, index=future_index)
	
  return forecast_s

def init_forecast(df, periods=5):
  
  future_index = np.arange(df.index.max() + 1, df.index.max() + periods + 1)
  forecast = pd.DataFrame(index=future_index)

  return forecast


def add_drivers(df, forecast, periods=5):
  
  payment_volume = df["PaymentVolume"]
  transactions = df["Transactions"]
	
  forecast["PaymentVolume"] = forecast_series(payment_volume, periods)
  forecast["Transactions"] = forecast_series(transactions, periods)

  return forecast


def add_revenue(df, forecast, periods=5, method="regression"):
  
  take_rate = df["Revenue"] / df["PaymentVolume"]

  if method == "mean":
    tr_forecast = pd.Series(
        [take_rate.tail(3).mean()] * periods,
        index=forecast.index
        )
  else:
    tr_forecast = forecast_series(take_rate, periods)

  forecast["Revenue"] = forecast["PaymentVolume"] * tr_forecast

  return forecast
	

def build_forecast(df, periods=5):
  
  forecast = init_forecast(df, periods)
  
  forecast = add_drivers(df, forecast, periods)

  forecast = add_revenue(df, forecast, periods)

  forecast = forecast.clip(lower=0)
  forecast = forecast.round(0)

  return forecast
