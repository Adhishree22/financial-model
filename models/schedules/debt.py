
import numpy as np
import pandas as pd

def build_debt_schedule(df, forecast):

    ebitda_margin = (df["EBITDA"] / df["Revenue"]).replace([np.inf, -np.inf], np.nan).mean()
    forecast["EBITDA"] = forecast["Revenue"] * ebitda_margin

    target_leverage = (df["TotalDebt"] / df["EBITDA"]).replace([np.inf, -np.inf], np.nan).median()
    int_rate = (df["Interest"] / df["TotalDebt"]).replace([np.inf, -np.inf], np.nan).median()
    std_ratio = (
        (df["ShortTermDebt"] / df["TotalDebt"])
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
        .median()
    )
    std_ratio = np.clip(std_ratio, 0, 1)

    #It captures residual financing flows not explicitly modeled (FX, leases, timing differences), scaled to revenue.
    debt_adjustment_hist = (df["TotalDebt"].diff() - (df["DebtIssued"] + df["Repayment"]))
    dadj_ratio = (debt_adjustment_hist / df["Revenue"]).mean()
    forecast["DebtAdjustment"] = forecast["Revenue"] * dadj_ratio

    target_hist = df["EBITDA"] * target_leverage
    gap = target_hist.shift(1) - df["TotalDebt"].shift(1)
    change = df["TotalDebt"].diff()

    adjustment_speed = ((change / gap).replace([np.inf, -np.inf], np.nan).dropna().median())
    adjustment_speed = max(0.1, min(adjustment_speed, 0.5))

    total_debt_list = []
    ltd_list = []
    std_list = []
    interest_list = []
    issued_list = []
    repayment_list = []

    opening_total_debt = df["TotalDebt"].iloc[-1]
    opening_std = df["ShortTermDebt"].iloc[-1]

    for year in forecast.index:

        repayment_std = -opening_std
        target_debt = forecast.loc[year, "EBITDA"] * target_leverage

        debt_adjustment = forecast.loc[year, "DebtAdjustment"]

        net_borrowing = adjustment_speed * (target_debt - opening_total_debt)

        issued = max(net_borrowing, 0)
        extra_repayment = min(net_borrowing, 0)
        repayment = repayment_std + extra_repayment

        closing_total_debt = (opening_total_debt + issued + repayment + debt_adjustment)

        closing_std = closing_total_debt * std_ratio
        closing_ltd = closing_total_debt - closing_std

        avg_debt = (opening_total_debt + closing_total_debt) / 2
        interest = avg_debt * int_rate

        total_debt_list.append(closing_total_debt)
        ltd_list.append(closing_ltd)
        std_list.append(closing_std)
        interest_list.append(interest)
        issued_list.append(issued)
        repayment_list.append(repayment)

        opening_total_debt = closing_total_debt
        opening_std = closing_std

    forecast["TotalDebt"] = total_debt_list
    forecast["LongTermDebt"] = ltd_list
    forecast["ShortTermDebt"] = std_list
    forecast["Interest"] = interest_list
    forecast["DebtIssued"] = issued_list
    forecast["Repayment"] = repayment_list

    return forecast
