
def build_investment_thesis(decision_df,results_df):
  
  catalysts = []
  risks = []
	
	# Strong upside
  if decision_df["Upside_Target%"] > 25:
    catalysts.append(f"Strong valuation upside (~{round(decision_df['upside_target'],1)}%)")
		
	# Improving business quality
  if decision_df["Terminal_Quality"] > decision_df["Base_Quality"]:
    catalysts.append("Improving business quality over time")
		
  # Risk improving
  if decision_df["Terminal_Risk"] < decision_df["Base_Risk"]:
    catalysts.append("Declining risk profile")
     
	# Growth acceleration signal 
  if decision_df["Terminal_Growth"] > decision_df["Base_Growth"]:
    catalysts.append("Potential growth acceleration")
    
	# Valuation convergence
  if decision_df["Upside_Blended%"] > 20:
    catalysts.append("Valuation multiple expansion potential")

    
	# Weak base quality
  if decision_df["Base_Quality"] < 55:
    risks.append("Moderate/weak current business quality")
    
	# Weak growth
  if decision_df["Base_Growth"] < 50:
    risks.append("Suboptimal growth profile")
    
	# High current risk
  if decision_df["Base_Risk"] > 50:
    risks.append("Elevated current risk levels")

  # DCF dependency
  terminal_weight = results_df.loc["Base", "TerminalWeight"]
  
  if terminal_weight > 0.85:
    risks.append("High dependence on terminal value assumptions")
    
	# Overvaluation risk
  if decision_df["Upside_DCF%"] < 10:
    risks.append("Limited margin of safety")

  decision_df["Catalysts"] = ", ".join(catalysts)
  decision_df["Risks"] = ", ".join(risks)

  return decision_df
