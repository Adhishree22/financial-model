
import pandas as pd
import numpy as np

def build_dcf_sensitivity(fcf, wacc, terminal_growth, years, net_debt, shares):
  
  fcf = np.array(fcf)
  n = len(fcf)

  # Ranges
  wacc_range = np.linspace(wacc - 0.01, wacc + 0.01, 5)
  growth_range = np.linspace(terminal_growth - 0.01, terminal_growth + 0.01, 5)

  sensitivity_table = pd.DataFrame(
      index=np.round(wacc_range, 4),
      columns=np.round(growth_range, 4)
  )

  for r in wacc_range:
    for g in growth_range:
      
      # Avoid invalid case
      if r <= g:
        sensitivity_table.loc[round(r, 4), round(g, 4)] = np.nan
        continue

      # Discount FCF
      discount_factors = 1 / (1 + r) ** years
      pv_fcf = np.sum(fcf * discount_factors)

      # Terminal value
      terminal_value = fcf[-1] * (1 + g) / (r - g)
      pv_terminal = terminal_value / (1 + r) ** n

      # EV → Equity → Price
      ev = pv_fcf + pv_terminal
      equity_value = ev - net_debt
      price = equity_value / shares

      sensitivity_table.loc[round(r, 4), round(g, 4)] = round(price, 2)
      
  sensitivity_table.index.name = "WACC ↓"
  sensitivity_table.columns.name = "Terminal Growth →"
  
  return sensitivity_table
