

import pandas as pd

Scale = 1000000

def scale_numeric_columns(df, skip_cols=None):

    df = df.copy()

    if skip_cols is None:
        skip_cols = []

    numeric_cols = [
        col for col in df.columns
        if col not in skip_cols
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    df[numeric_cols] = df[numeric_cols] * Scale

    return df


def sort_dataframe(df):
  
  df = df.copy()

  # If Year exists as a column
  if "Year" in df.columns:
    df = df.sort_values("Year").reset_index(drop=True)

  # If Year exists in index
  elif df.index.name == "Year":
    df = df.sort_index().reset_index()

  return df


def prepare_year_column(df):

    df = df.copy()

    # If index itself is Year
    if df.index.name == "Year":

        df = df.reset_index()

    # If DatetimeIndex exists
    elif isinstance(df.index, pd.DatetimeIndex):

        df["Year"] = df.index.year
        df = df.reset_index(drop=True)

    return df
	
	
def export_single_dataframe(df, filename, skip_cols=None):

  # If no skip columns provided
  if skip_cols is None:
    skip_cols = []
	
  df = prepare_year_column(df)
  df = scale_numeric_columns(df, skip_cols)
  df = sort_dataframe(df)

  path = f"dashboard/{filename}.csv"

  df.to_csv(path, index=False)

  print(f"{filename}.csv - {df.shape}")

  return df


def export_for_tableau(
    historical_data,
    full_df,
    growth_df,
    ratios_df,
    valuation_df,
    diagnostic_df,
    results_df,
    valuation_summary,
    sensitivity_table,
    quality_df,
    risk_df,
    growth_score_df,
    composite_df,
    decision_df,
    driver_scenario_df
):

  exported = {}

  historical_skip = ['Closing', 'Shares', 'EPS', 'Check']
  exported["historical_data"] = export_single_dataframe(historical_data, "historical_data", historical_skip)

  full_skip = ['Closing', 'Shares', 'EPS', 'Check',"DPS"]
  exported["full_df"] = export_single_dataframe(full_df, "full_df", full_skip)

  exported["growth_df"] = export_single_dataframe(growth_df, "growth_df")

  exported["ratios_df"] = export_single_dataframe(ratios_df, "ratios_df")

  exported["valuation_df"] = export_single_dataframe(valuation_df, "valuation_df")

  exported["diagnostic_df"] = export_single_dataframe( diagnostic_df, "diagnostic_df")

  exported["results_df"] = export_single_dataframe(results_df, "results_df")

  exported["valuation_summary"] = export_single_dataframe(valuation_summary, "valuation_summary")

  exported["sensitivity_table"] = export_single_dataframe(sensitivity_table, "sensitivity_table")

  exported["quality_df"] = export_single_dataframe(quality_df, "quality_df")
	
  exported["risk_df"] = export_single_dataframe(risk_df, "risk_df")

  exported["growth_score_df"] = export_single_dataframe(growth_score_df, "growth_score_df")

  exported["composite_df"] = export_single_dataframe(composite_df, "composite_df")

  exported["decision_df"] = export_single_dataframe(decision_df, "decision_df")

  exported["driver_scenario_df"] = export_single_dataframe(driver_scenario_df, "driver_scenario_df")

  print("\nAll Tableau exports completed successfully.")

  return exported
