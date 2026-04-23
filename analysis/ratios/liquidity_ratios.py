
import numpy as np
import pandas as pd

def build_liquidity_ratios(full_df,ratios_df):
  
  # Current Ratio
  ratios_df['CurrentRatio'] = full_df['CurrentAssets'] / full_df['CurrentLiabilities'].replace(0, np.nan)

  # Quick Ratio
  ratios_df['QuickRatio'] = (full_df['EndingCash'] + full_df['CashAdjustment'] + full_df['Receivables'] + full_df['RestrictedCash']) / full_df['CurrentLiabilities'].replace(0, np.nan)

  # Cash Ratio
  ratios_df['CashRatio'] = (full_df['EndingCash'] + full_df['CashAdjustment']) / full_df['CurrentLiabilities'].replace(0, np.nan)

  ratios_df.replace([np.inf, -np.inf], np.nan, inplace=True)
	ratios_df = ratios_df.round(2)
	
  return ratios_df
