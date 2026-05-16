

import pandas as pd

Scale = 1000000

def scale_numeric_columns(df, skip_cols):

    df = df.copy()

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

  return df


def prepare_year_column(df):

    df = df.copy()

    if pd.api.types.is_integer_dtype(df.index):

        df = df.reset_index()

        # Rename created index column to Year
        df.rename(columns={"index": "Year"}, inplace=True)
		
    # If DatetimeIndex exists
    elif isinstance(df.index, pd.DatetimeIndex):

        df["Year"] = df.index.year
        df = df.reset_index(drop=True)
		
    return df
	
	
def export_single_dataframe(df, filename, skip_cols=None):

  # If no skip columns provided
  if skip_cols is None:
    skip_cols = []
	
  df = scale_numeric_columns(df, skip_cols)
  df = prepare_year_column(df)
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

  historical_skip = ['Year','Closing', 'Shares', 'EPS', 'Check']
  exported["historical_data"] = export_single_dataframe(historical_data, "historical_data", historical_skip)

  full_skip = ['Closing', 'Shares', 'EPS', 'Check',"DPS"]
  exported["full_df"] = export_single_dataframe(full_df, "full_df", full_skip)
  
  growth_skip = growth_df.columns.to_list()
  exported["growth_df"] = export_single_dataframe(growth_df, "growth_df", growth_skip)
  
  ratios_skip = ratios_df.columns.to_list()
  exported["ratios_df"] = export_single_dataframe(ratios_df, "ratios_df", ratios_skip)
  
  val_skip = valuation_df.columns.to_list()
  exported["valuation_df"] = export_single_dataframe(valuation_df, "valuation_df",val_skip)
  
  diag_skip = diagnostic_df.columns.to_list()
  exported["diagnostic_df"] = export_single_dataframe( diagnostic_df, "diagnostic_df", diag_skip)
  
  results_skip = results_df.columns.to_list()
  exported["results_df"] = export_single_dataframe(results_df, "results_df", results_skip)
  
  valuation_summary = valuation_summary.reset_index()
  valuation_summary.rename(columns={valuation_summary.columns[0]: "Scenario"}, inplace=True)	
  valsum_skip = valuation_summary.columns.to_list()
  exported["valuation_summary"] = export_single_dataframe(valuation_summary, "valuation_summary", valsum_skip)
  
  sensitivity_table = sensitivity_table.reset_index()
  sensitivity_table.rename(columns={sensitivity_table.columns[0]: "WACC"}, inplace=True)
  sensitivity_table = sensitivity_table.melt(
      id_vars="WACC",
      var_name="TerminalGrowth",
      value_name="Price"
  )
  sens_skip = sensitivity_table.columns.to_list()
  exported["sensitivity_table"] = export_single_dataframe(sensitivity_table, "sensitivity_table",sens_skip)

  score_df = pd.merge(quality_df,risk_df, left_index=True,right_index=True)
  score_df = pd.merge(score_df,growth_score_df, left_index=True,right_index=True)
  score_df = pd.merge(score_df,composite_df, left_index=True,right_index=True)
  score_df = score_df.loc[:, ~score_df.columns.str.endswith('_y')]
  score_df.columns = [col.replace('_x', '') for col in score_df.columns]
  score_skip = score_df.columns.to_list()
  exported["score_df"] = export_single_dataframe(score_df, "score_df", score_skip)
  
  decision_skip = decision_df.columns.to_list()
  exported["decision_df"] = export_single_dataframe(decision_df, "decision_df", decision_skip)
  
  driver_skip = driver_scenario_df.columns.to_list()
  exported["driver_scenario_df"] = export_single_dataframe(driver_scenario_df, "driver_scenario_df", driver_skip)

  print("\nAll Tableau exports completed successfully.")

  return exported
