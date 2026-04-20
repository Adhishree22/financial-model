
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

    forecast = pd.Series(pred, index=future_index)

    return forecast


def forecast_drivers(df, periods=5):

    payment_volume = df["PaymentVolume"]
    transactions = df["Transactions"]

    forecast = pd.DataFrame()

    forecast["PaymentVolume"] = forecast_series(payment_volume, periods)
    forecast["Transactions"] = forecast_series(transactions, periods)

    return forecast


def forecast_take_rate(df, periods=5, method="regression"):

    take_rate = df["Revenue"] / df["PaymentVolume"]

    last_year = df.index.max()
    future_index = np.arange(last_year + 1, last_year + periods + 1)

    if method == "regression":
        tr_forecast = forecast_series(take_rate, periods)

    elif method == "mean":
        # safer option (recommended)
        avg = take_rate.tail(3).mean()
        tr_forecast = pd.Series([avg] * periods, index=future_index)

    else:
        raise ValueError("Invalid method")

    return tr_forecast


def forecast_revenue(df, forecast, periods=5):

    take_rate_forecast = forecast_take_rate(df, periods)

    forecast["Revenue"] = (
        forecast["PaymentVolume"] * take_rate_forecast
    )

    return forecast


def build_forecast(df, periods=5):

    forecast = forecast_drivers(df, periods)

    forecast = forecast_revenue(df, forecast, periods)

    # Guardrails (important)
    forecast = forecast.clip(lower=0)

    return forecast.round(0)
