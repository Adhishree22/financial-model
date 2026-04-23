
import pandas as pd
from .core import run_valuation_scenario

def run_ev_valuation(df, forecast, full_df):
  
  valuation_df = pd.DataFrame()
	
  market_hist = (df["Closing"] * df["Shares"]).round(2)
  ev = market_hist + (df["NetDebt"] * 1000000)

  ev_ebitda = run_valuation_scenario(ev, full_df["EBITDA"], df, forecast, "EV_EBITDA", equity=False)
  ev_rev = run_valuation_scenario(ev, full_df["Revenue"], df, forecast, "EV_Revenue", equity=False)
  ev_ebit = run_valuation_scenario(ev, full_df["OperatingIncome"], df, forecast, "EV_EBIT", equity=False)
  
  valuation_df = pd.concat([ev_ebitda, ev_rev, ev_ebit], axis=1)
  
  return valuation_df
