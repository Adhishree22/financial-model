
import pandas as pd

def build_driver_scenarios(growth_df):
  
  scenarios = {
      "Bear": {
          "rev_adj": -2.0,
          "margin_adj": -1.0,
          "cashflow_adj": -1.5
      },
      "Base": {
          "rev_adj": 0.0,
          "margin_adj": 0.0,
          "cashflow_adj": 0.0
      },
      "Bull": {
          "rev_adj": 2.5,
          "margin_adj": 1.0,
          "cashflow_adj": 1.5
      }
  }
  
  driver_outputs = []
  
  for scenario_name, adj in scenarios.items():
    
    driver_df = growth_df.copy()

    # ---------------- Revenue Shock ----------------
    if "Revenue_Growth%" in driver_df.columns:
      driver_df["Revenue_Growth%"] = driver_df["Revenue_Growth%"] + adj["rev_adj"]

    # ---------------- Profitability Shock ----------------
    for col in ["OperatingIncome_Growth%", "NetIncome_Growth%", "EPS_Growth%"]:
      if col in driver_df.columns:
        driver_df[col] = driver_df[col] + adj["rev_adj"] * 0.8

    # ---------------- Margin Shock ----------------
    if "OperatingMargin_Change" in driver_df.columns:
      driver_df["OperatingMargin_Change"] = driver_df["OperatingMargin_Change"] + adj["margin_adj"]

    # ---------------- Cash Flow Shock ----------------
    for col in ["FreeCashFlow_Growth%", "OperatingCashFlow_Growth%"]:
      if col in driver_df.columns:
        driver_df[col] = driver_df[col] + adj["cashflow_adj"]

    # ---------------- Scenario Tag ----------------
    driver_df["Scenario"] = scenario_name
    
    driver_outputs.append(driver_df)
    
  driver_scenario_df = pd.concat(driver_outputs)
  driver_scenario_df = driver_scenario_df.round(4)
  
  return driver_scenario_df

