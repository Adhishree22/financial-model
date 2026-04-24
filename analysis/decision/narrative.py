
def build_investment_thesis(decision_df,results_df):
  
  catalysts = []
  risks = []
	
	# Strong upside
  if decision_df["upside_target"] > 25:
    catalysts.append(f"Strong valuation upside (~{round(decision_df['upside_target'],1)}%)")
		
	# Improving business quality
  if decision_df["terminal_quality"] > decision_df["base_quality"]:
    catalysts.append("Improving business quality over time")
		
  # Risk improving
  if decision_df["terminal_risk"] < decision_df["base_risk"]:
    catalysts.append("Declining risk profile")
     
	# Growth acceleration signal 
  if decision_df["terminal_growth"] > decision_df["base_growth"]:
    catalysts.append("Potential growth acceleration")
    
	# Valuation convergence
  if decision_df["upside_blended"] > 20:
    catalysts.append("Valuation multiple expansion potential")

    
	# Weak base quality
  if decision_df["base_quality"] < 55:
    risks.append("Moderate/weak current business quality")
    
	# Weak growth
  if decision_df["base_growth"] < 50:
    risks.append("Suboptimal growth profile")
    
	# High current risk
  if decision_df["base_risk"] > 50:
    risks.append("Elevated current risk levels")

  # DCF dependency
  terminal_weight = results_df.loc["Base", "TerminalWeight"]
  
  if decision_df["terminal_weight"] > 0.85:
    risks.append("High dependence on terminal value assumptions")
    
	# Overvaluation risk
  if decision_df["upside_dcf"] < 10:
    risks.append("Limited margin of safety")

  decision_df["Catalysts"] = ", ".join(catalysts)
  decision_df["Risks"] = ", ".join(risks)

  return decision_df
