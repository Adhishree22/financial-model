
import numpy as np
import pandas as pd

def build_ppe_schedule(df, forecast):

    capex_ratio = (df["Capex"] / df["Revenue"]).mean()
    depr_rate = (df["Depreciation"] / df["PPE"]).replace([np.inf, -np.inf], 0).mean()


	df["PPEAdjustment"] = (df["PPE"].diff()- ((-df["Capex"]) - df["Depreciation"]))
	padj_ratio = (df["PPEAdjustment"] / df["Revenue"]).mean()
	forecast["PPEAdjustment"] = forecast["Revenue"] * padj_ratio

    ppe_list = []
    dep_list = []
    capex_list = []

    opening_ppe = df["PPE"].iloc[-1]

    for year in forecast.index:

        capex = forecast.loc[year, "Revenue"] * capex_ratio
        adjustment = forecast.loc[year, "PPEAdjustment"]

        depreciation = opening_ppe * depr_rate

        closing_ppe = opening_ppe - capex - depreciation + adjustment

        capex_list.append(capex)
        dep_list.append(depreciation)
        ppe_list.append(closing_ppe)

        opening_ppe = closing_ppe

    forecast["Capex"] = capex_list
    forecast["Depreciation"] = dep_list
    forecast["PPE"] = ppe_list

    return forecast
