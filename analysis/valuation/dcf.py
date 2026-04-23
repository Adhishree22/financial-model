
# analysis/valuation/dcf_valuation.py

import numpy as np
import pandas as pd

def compute_wacc(df, forecast, beta):
  
  #Assumptions
  risk_free_rate = 0.07
  market_premium = 0.05
  
  cost_of_debt = (df["Interest"] / df["TotalDebt"]).replace([np.inf, -np.inf], np.nan).dropna().mean()

  tax_rate = (df["Taxes"] / df["EBT"]).replace([np.inf, -np.inf], np.nan).dropna().mean()

  debt = forecast["TotalDebt"].iloc[-3:].mean() * 1000000
  equity = forecast["Equity"].iloc[-3:].mean() * 1000000
	
	#Capital Structure
  total_capital = debt + equity
  w_d = debt / total_capital
  w_e = equity / total_capital
	
	#Base WACC
  cost_of_equity = risk_free_rate + beta * market_premium
  after_tax_cod = cost_of_debt * (1 - tax_rate)

  wacc = w_e * cost_of_equity + w_d * after_tax_cod

  return wacc, cost_of_equity, cost_of_debt


def run_dcf(forecast, wacc, terminal_growth):
  
  fcf = (forecast["FreeCashFlow"].replace([np.inf, -np.inf], np.nan).dropna()) * 1000000
  fcf = fcf.values
	
  n = len(fcf)
  years = np.arange(1, n + 1)

  net_debt = forecast["NetDebt"].iloc[-1] * 1000000
  shares = forecast["Shares"].iloc[-1]

  discount_factors = 1 / (1 + wacc) ** years
  pv_fcf = np.sum(fcf * discount_factors)

  terminal_value = fcf[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
  pv_terminal = terminal_value / (1 + wacc) ** n

  ev = pv_fcf + pv_terminal
  equity_value = ev - net_debt
  price = equity_value / shares

  terminal_weight = pv_terminal / ev

  return {
      "EV": ev,
      "Equity": equity_value,
      "Price": price,
      "TerminalWeight": terminal_weight
  }



def run_dcf_scenarios(forecast, wacc, terminal_growth):
  
  scenarios = {
    "Low": {"wacc": wacc + 0.005, "growth": terminal_growth - 0.005},
    "Base": {"wacc": wacc, "growth": terminal_growth},
    "High": {"wacc": wacc - 0.005, "growth": terminal_growth + 0.005}
  }

  results = {}

  for name, vals in scenarios.items():
    results[name] = run_dcf(
        forecast,
        vals["wacc"],
        vals["growth"]
      )

  return pd.DataFrame(results).T.round(2)
