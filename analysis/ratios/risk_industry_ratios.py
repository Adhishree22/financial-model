
import numpy as np
import pandas as pd


def build_risk_industry_ratios(full_df, ratios_df,growth_df):
  
  #Macro / Risk Sensitivity

  #FX Sensitivity (Revenue growth vs volume growth)
  ratios_df["Revenue_vs_Volume_Gap"] = growth_df["Revenue_Growth%"] - growth_df["PaymentVolume_Growth%"]

  # Cost Rigidity (How fast costs grow vs revenue)
  ratios_df["Cost_Rigidity"] = (growth_df["OperatingExpense_Growth%"] / growth_df["Revenue_Growth%"].replace(0, np.nan)) * 100

  # Debt to FCF (Years of FCF to repay debt)
  ratios_df["Debt_to_FCF_Years"] = (full_df["TotalDebt"] / full_df["FreeCashFlow"].replace(0, np.nan))

  # Take Rate (Core monetization metric)
  ratios_df["Take_Rate_%"] = (full_df["Revenue"] / full_df["PaymentVolume"] ) * 100

  # Revenue per Transaction
  ratios_df["Revenue_per_Transaction"] = (full_df["Revenue"] / full_df["Transactions"])

  # Average Ticket Size
  ratios_df["Avg_Ticket_Size"] = (full_df["PaymentVolume"] / full_df["Transactions"])

  # Transactions per Dollar (inverse of ticket size)
  ratios_df["Transactions_per_Dollar"] = (full_df["Transactions"] / full_df["PaymentVolume"])

  ratios_df = ratios_df.round(5)
  ratios_df.replace([np.inf, -np.inf], np.nan, inplace=True)
  
  return ratios_df
