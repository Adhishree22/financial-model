
import numpy as np
import pandas as pd

def build_income_statement(df, forecast):

    cost_rev_ratio = (df["CostOfRevenue"] / df["Revenue"]).mean()
    forecast["CostOfRevenue"] = forecast["Revenue"] * cost_rev_ratio

    forecast["GrossProfit"] = forecast["Revenue"] - forecast["CostOfRevenue"]

    opex_ratio = (df["OperatingExpense"] / df["Revenue"]).mean()
    forecast["OperatingExpense"] = forecast["Revenue"] * opex_ratio

    forecast["OperatingIncome"] = (forecast["Revenue"] - forecast["CostOfRevenue"] - forecast["OperatingExpense"])

    other_exp_ratio = (df["OtherExpense"] / df["Revenue"]).median()
    forecast["OtherExpense"] = forecast["Revenue"] * other_exp_ratio

    forecast["EBT"] = (forecast["OperatingIncome"] + forecast["OtherExpense"] - forecast["Interest"])

    tax_rate = (df["Taxes"] / df["EBT"]).mean()
    forecast["Taxes"] = np.where(forecast["EBT"] > 0, forecast["EBT"] * tax_rate, 0)

    forecast["NetIncome"] = forecast["EBT"] - forecast["Taxes"]

    return forecast
