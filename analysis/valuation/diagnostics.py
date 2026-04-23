
import pandas as pd
import numpy as np

def build_diagnostics(valuation_df, df, forecast):
  
  diagnostic_df = pd.DataFrame(index=valuation_df.index)
	
  diagnostic_df = valuation_df[[ 
      "Expected_Return_PE%", "Valuation_Gap_PE%",
      "Expected_Return_PS%", "Valuation_Gap_PS%",
      "Expected_Return_PB%", "Valuation_Gap_PB%",
      "Expected_Return_EV_EBITDA%", "Valuation_Gap_EV_EBITDA%",
      "Expected_Return_EV_Revenue%","Valuation_Gap_EV_Revenue%",
      "Expected_Return_EV_EBIT%", "Valuation_Gap_EV_EBIT%",
      "Expected_Return_FCF_Yield%", "Valuation_Gap_FCF_Yield%",
      "Expected_Return_Div_Yield%","Valuation_Gap_Div_Yield%"
  ]].copy()

  diagnostic_df["Valuation_Gap_Hist%"] = np.nan
  diagnostic_df.loc[df.index, "Valuation_Gap_Hist%"] = ((valuation_df.loc[df.index, "Blended_Price"] / df["Closing"] - 1) * 100).round(2)

  diagnostic_df["Upside_Blended%"] = np.nan
  diagnostic_df.loc[forecast.index, "Upside_Blended%"] = ((valuation_df.loc[forecast.index, "Blended_Price"] / df["Closing"].iloc[-1] - 1) * 100).round(2)
  
  base_year = df.index[-1] # last historical year (2025)
  diagnostic_df["Years"] = valuation_df.index - base_year

  mask = diagnostic_df["Years"] > 0
  diagnostic_df["Annualized_Return_%"] = np.nan
  diagnostic_df.loc[mask, "Annualized_Return_%"] = (
      (valuation_df.loc[mask, "Blended_Price"] / df["Closing"].iloc[-1])
      ** (1 / diagnostic_df.loc[mask, "Years"]) - 1) * 100
      
  diagnostic_df["Annualized_Return_%"] = diagnostic_df["Annualized_Return_%"].round(2)

  return diagnostic_df
