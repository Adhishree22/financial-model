
import numpy as np
import pandas as pd


def build_cashflow_ratios(full_df, ratios_df):
  
  # Core
  ratios_df["FCF_to_Revenue"] = full_df["FreeCashFlow"] / full_df["Revenue"].replace(0, np.nan)
  ratios_df["OCF_to_Revenue"] = full_df["OperatingCashFlow"] / full_df["Revenue"].replace(0, np.nan)
  ratios_df["Capex_to_Revenue"] = abs(full_df["Capex"]) / full_df["Revenue"].replace(0, np.nan)

  # Conversion / Quality
  ratios_df["FCF_Conversion"] = full_df["FreeCashFlow"] / full_df["NetIncome"].replace(0, np.nan)
  ratios_df["OCF_to_NetIncome"] = full_df["OperatingCashFlow"] / full_df["NetIncome"].replace(0, np.nan)

  # Advanced
  ratios_df["FCF_to_EBITDA"] = full_df["FreeCashFlow"] / full_df["EBITDA"].replace(0, np.nan)
  ratios_df["Cash_Conversion"] = full_df["OperatingCashFlow"] / full_df["EBITDA"].replace(0, np.nan)
  ratios_df["Capex_Coverage"] = full_df["OperatingCashFlow"] / abs(full_df["Capex"])

  # Per Share
  ratios_df["FCF_per_Share"] = (full_df["FreeCashFlow"] * 1000000) / full_df["Shares"]  
		   
  ratios_df.replace([np.inf, -np.inf], np.nan, inplace=True)
	ratios_df = ratios_df.round(2)
	
  return ratios_df
