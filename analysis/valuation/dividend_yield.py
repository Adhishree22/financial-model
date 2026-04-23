
import numpy as np
import pandas as pd


def run_dividend_yield_valuation(dps_series, hist_df, forecast, name = "Div_Yield"):

    historical = pd.DataFrame(index=hist_df.index)
    forecast_df = pd.DataFrame(index=forecast.index)

    w_bear, w_base, w_bull = 0.25, 0.5, 0.25

    dps_hist = dps_series.reindex(hist_df.index)
    dps_fore = dps_series.reindex(forecast.index)

    historical[name] = (dps_hist / hist_df["Closing"]).round(4)

    low = historical[name].rolling(3, min_periods=1).quantile(0.25)
    high = historical[name].rolling(3, min_periods=1).quantile(0.75)

    historical["Price_Low"] = dps_hist / high
    historical["Price_Base"] = hist_df["Closing"]
    historical["Price_High"] = dps_hist / low

    start = historical[name].iloc[-1]
    target = historical[name].tail(3).median()

    forecast_df[name] = np.linspace(start, target, len(forecast))

    low_f = historical[name].tail(3).quantile(0.25)
    high_f = historical[name].tail(3).quantile(0.75)

    forecast_df["Price_Low"] = dps_fore / high_f
    forecast_df["Price_Base"] = dps_fore / forecast_df[name]
    forecast_df["Price_High"] = dps_fore / low_f

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
    forecast_df["Expected_Return_%"] = (
        (forecast_df["Expected_Price"] / current_price - 1) * 100
    )

    historical["Valuation_Gap_%"] = (
        (historical["Expected_Price"] / historical["Price_Base"] - 1) * 100
    )

    forecast_df["Valuation_Gap_%"] = (
        (forecast_df["Expected_Price"] / forecast_df["Price_Base"] - 1) * 100
    )

    output = pd.concat([historical, forecast_df]).replace([np.inf, -np.inf], np.nan).round(2)

    final = pd.DataFrame(index=output.index)

    final[name] = output[name]
    final[f"Expected_Price_{name}"] = output["Expected_Price"]
    final[f"Expected_Return_{name}%"] = output["Expected_Return_%"]
    final[f"Valuation_Gap_{name}%"] = output["Valuation_Gap_%"]

    return final
