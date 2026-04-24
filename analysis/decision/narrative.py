
def build_investment_thesis(decision_df,results_df):
  
  catalysts = []
  risks = []
  row = decision_df.iloc[0]

	# Strong upside
  if row["Upside_Target%"] > 25:
    catalysts.append(f"Strong valuation upside (~{round(row["Upside_Target%"],1)}%)")
		
	# Improving business quality
  if row["Terminal_Quality"] > row["Base_Quality"]:
    catalysts.append("Improving business quality over time")
		
  # Risk improving
  if row["Terminal_Risk"] < row["Base_Risk"]:
    catalysts.append("Declining risk profile")
     
	# Growth acceleration signal 
  if row["Terminal_Growth"] > row["Base_Growth"]:
    catalysts.append("Potential growth acceleration")
    
	# Valuation convergence
  if row["Upside_Blended%"] > 20:
    catalysts.append("Valuation multiple expansion potential")

    
	# Weak base quality
  if row["Base_Quality"] < 55:
    risks.append("Moderate/weak current business quality")
    
	# Weak growth
  if row["Base_Growth"] < 50:
    risks.append("Suboptimal growth profile")
    
	# High current risk
  if row["Base_Risk"] > 50:
    risks.append("Elevated current risk levels")

  # DCF dependency
  terminal_weight = results_df.loc["Base", "TerminalWeight"]
  
  if terminal_weight > 0.85:
    risks.append("High dependence on terminal value assumptions")
    
	# Overvaluation risk
  if row["Upside_DCF%"] < 10:
    risks.append("Limited margin of safety")

  decision_df["Catalysts"] = ", ".join(catalysts)
  decision_df["Risks"] = ", ".join(risks)

  return decision_df
