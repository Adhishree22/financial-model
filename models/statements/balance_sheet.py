
import numpy as np
import pandas as pd

def build_balance_sheet(df, forecast):
  
  inva_ratio = (df["InvestmentsAndAdvances"] / df["Revenue"]).tail(3).mean()
  forecast["InvestmentsAndAdvances"] = forecast["Revenue"] * inva_ratio
  
  onca_ratio = (df["OtherNonCurrentAssets"] / df["Revenue"]).median()
  forecast["OtherNonCurrentAssets"] = forecast["Revenue"] * onca_ratio
  
  oncl_ratio = (df["OtherNonCurrentLiabilities"] / df["Revenue"]).median()
  forecast["OtherNonCurrentLiabilities"] = forecast["Revenue"] * oncl_ratio
  
  opening = df["NonCurrentDeferredLiabilities"].iloc[-1]
  
  dt_list = []
  for year in forecast.index:
    opening = opening + forecast.loc[year, "DeferredTax"]
    dt_list.append(opening)

  forecast["NonCurrentDeferredLiabilities"] = dt_list

	forecast = forecast.round(0)
	
  forecast["TotalAssets"] = (
      forecast["CurrentAssets"]
      + forecast["PPE"]
      + forecast["GoodwillAndOtherIntangibleAssets"]
      + forecast["OtherNonCurrentAssets"]
      + forecast["InvestmentsAndAdvances"]
  )


  forecast["TotalLiabilities"] = (
      forecast["CurrentLiabilities"]
      + forecast["LongTermDebt"]
      + forecast["OtherNonCurrentLiabilities"]
      + forecast["NonCurrentDeferredLiabilities"]
  )

	df["BalanceSheetAdjustment"] = df["Equity"] + df["TotalLiabilities"] - df["TotalAssets"]
	forecast["BalanceSheetAdjustment"] = (forecast["Equity"] + forecast["TotalLiabilities"] - forecast["TotalAssets"])

  return forecast


def sanity_check(df,forecast):

  df["Check"] = df["Equity"] + df["TotalLiabilities"] - ( df["TotalAssets"] + df["BalanceSheetAdjustment"])
  forecast["Check"] = forecast["Equity"] + forecast["TotalLiabilities"] - (forecast["TotalAssets"] + forecast["BalanceSheetAdjustment"])
  forecast["Check"] = forecast["Check"].apply(lambda x: 0 if np.isclose(x, 0, atol=1) else x)

  return forecast
