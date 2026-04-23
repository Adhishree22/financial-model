
import pandas as pd
from .core import run_valuation_scenario

def run_equity_valuation(df, forecast, full_df):
  valuation_df = pd.DataFrame()
  
  #P/E ratio (Price / Earnings)
  pe = (df["Closing"] / df["EPS"]).round(2)
  eps_series = full_df["EPS"]
  pe_df = run_valuation_scenario(pe, eps_series, df, forecast, "PE", True)
  pe_df["EPS"] = eps_series
	
  #P/S Ratio (Price / Revenue per Share)
  rev_ps = ((full_df["Revenue"] * 1000000) / full_df["Shares"]).round(2)
  ps = (df["Closing"] / rev_ps.loc[df.index]).round(2)
  ps_df = run_valuation_scenario(ps, rev_ps, df, forecast, "PS", True)
  ps_df["Revenue_per_Share"] = rev_ps
	
  #P/B Ratio (Price / Book Value per Share)
  bvps = (((full_df["Equity"] - full_df["PreferredStockEquity"]) * 1000000) / full_df["Shares"]).round(2)
  pb = (df["Closing"] / bvps.loc[df.index]).round(2)
  pb_df = run_valuation_scenario(pb, bvps, df, forecast, "PB", True)
  pb_df["BVPS"] = bvps
  
  valuation_df = pd.concat([pe_df, ps_df, pb_df], axis=1)
  
  return valuation_df
