
import numpy as np
import pandas as pd

def initialize_profitability_ratios(full_df,forecast_index):

  ratios_df = pd.DataFrame(index=full_df.index)

  # Core profitability margins
  ratios_df['NetProfitMargin'] = (full_df['NetIncome'] / full_df['Revenue']) * 100
  ratios_df['OperatingMargin'] = (full_df['OperatingIncome'] / full_df['Revenue']) * 100
  ratios_df['ROA'] = (full_df['NetIncome'] / full_df['TotalAssets']) * 100
  ratios_df['ROE'] = (full_df['NetIncome'] / full_df['Equity']) * 100
  ratios_df['EBITDAMargin'] = (full_df['EBITDA'] / full_df['Revenue']) * 100
  ratios_df['GrossMargin'] = (full_df['GrossProfit'] / full_df['Revenue']) * 100

  # Cash flow margins
  ratios_df["OCF_Margin%"] = (full_df["OperatingCashFlow"] / full_df["Revenue"]) * 100
  ratios_df["FCF_Margin%"] = (full_df["FreeCashFlow"] / full_df["Revenue"]) * 100

  # Cost structure
  ratios_df["Cost_Margin%"] = (full_df["CostOfRevenue"] / full_df["Revenue"]) * 100
  ratios_df["Opex_Margin%"] = (full_df["OperatingExpense"] / full_df["Revenue"]) * 100

  #Margin drift
  for col in ['OperatingMargin', 'EBITDAMargin', 'GrossMargin']:
    for year in forecast_index:
      ratios_df.loc[year, col] = ratios_df.loc[year - 1, col] * 1.002

  return ratios_df



def compute_margin_changes(ratios_df):

  ratios_df["Net_Margin_Change"] = ratios_df['NetProfitMargin'].diff()
  ratios_df["Operating_Margin_Change"] = ratios_df['OperatingMargin'].diff()
  ratios_df["EBITDA_Margin_Change"] = ratios_df['EBITDAMargin'].diff()
  ratios_df["OCF_Margin_Change"] = ratios_df["OCF_Margin%"].diff()
  ratios_df["FCF_Margin_Change"] = ratios_df["FCF_Margin%"].diff()

  return ratios_df


def compute_incremental_margins(full_df,ratios_df):

  delta_rev = full_df["Revenue"].diff().replace(0, np.nan)

  def incremental(metric):
    return (full_df[metric].diff() / delta_rev) * 100

  ratios_df["Incremental_Operating_Margin"] = incremental("OperatingIncome")
  ratios_df["Incremental_EBITDA_Margin"] = incremental("EBITDA")
  ratios_df["Incremental_Net_Margin"] = incremental("NetIncome")
  ratios_df["Incremental_FCF_Margin"] = incremental("FreeCashFlow")
  ratios_df["Incremental_OCF_Margin"] = incremental("OperatingCashFlow")

  return ratios_df


def build_profitability_ratios(full_df,forecast_index):

  ratios_df = initialize_profitability_ratios(full_df,forecast_index)

  ratios_df = compute_margin_changes(ratios_df)
  ratios_df = compute_incremental_margins(full_df, ratios_df)

  ratios_df = ratios_df.replace([np.inf, -np.inf], np.nan)
  ratios_df = ratios_df.round(2)

  return ratios_df
