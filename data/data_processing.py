
import pandas as pd
import numpy as np

Scale = 1000000

def safe_get(df, column, default=0):
  """Safely fetch column from dataframe"""
  return df[column] if column in df.columns else default

def build_historical_df(income, balance, cashflow, price_data):
  
  df = pd.DataFrame()

  #Income Statement
  df["Revenue"] = safe_get(income, "Total Revenue").ffill() / Scale
  df["CostOfRevenue"] = safe_get(income, "Cost Of Revenue").ffill() / Scale
  df["GrossProfit"] = safe_get(income, "Gross Profit").ffill() / Scale
  df["OperatingExpense"] = safe_get(income, "Operating Expense").ffill() / Scale
  df["OperatingIncome"] = safe_get(income, "Operating Income").fillna(df["Revenue"] - df["CostOfRevenue"] - df["OperatingExpense"]) / Scale
  df["OtherExpense"] = safe_get(income, "Other Income Expense").fillna(safe_get(income, "Other Income Expense").tail(3).mean()) / Scale
  df["EBT"] = safe_get(income, "Pretax Income").fillna(df["OperatingIncome"] + df["OtherExpense"]) / Scale
  df["Taxes"] = safe_get(income, "Tax Provision").ffill() / Scale
  df["NetIncome"] = safe_get(income, "Net Income").fillna(df["EBT"] - df["Taxes"]) / Scale

  #CashFlowOperating
  df["ChangeWC"] = safe_get(cashflow, "Change In Working Capital").ffill() / Scale
  df["OperatingCashFlow"] = safe_get(cashflow, "Operating Cash Flow").ffill() / Scale
  df["OtherNonCashItems"] = safe_get(cashflow, "Other Non Cash Items").ffill() / Scale
  df["AmortizationOfIntangibles"] = safe_get(cashflow, "Amortization Of Intangibles").ffill() / Scale
  df["DeferredTax"] = safe_get(cashflow, "Deferred Tax").fillna(safe_get(cashflow, "Deferred Tax").tail(3).mean()) / Scale
  df["GoodwillAndOtherIntangibleAssets"] = safe_get(balance, "Goodwill And Other Intangible Assets").ffill() / Scale
  df["OperatingGainsLosses"] = safe_get(cashflow, "Operating Gains Losses").fillna(
      safe_get(cashflow, "Operating Gains Losses").tail(3).mean()
  ) / Scale
	
	#CashFlowInvesting
  df["InvestingCashFlow"] = safe_get(cashflow, "Investing Cash Flow").ffill() / Scale
  df["NetInvestmentPurchaseAndSale"] = safe_get(cashflow, "Net Investment Purchase And Sale").ffill() / Scale
  df["NetBusinessPurchaseAndSale"] = safe_get(cashflow, "Net Business Purchase And Sale").fillna(0) / Scale
  df["NetOtherInvestingChanges"] = safe_get(cashflow, "Net Other Investing Changes").fillna(
      safe_get(cashflow, "Net Other Investing Changes").tail(3).mean()
  ) / Scale
	
	#CashFlowFinancing
  df["FinancingCashFlow"] = safe_get(cashflow, "Financing Cash Flow").ffill() / Scale
  df["NetOtherFinancingCharges"] = safe_get(cashflow, "Net Other Financing Charges").fillna(
      safe_get(cashflow, "Net Other Financing Charges").tail(3).mean()
  ) / Scale
	
	#Cash Flow
  df["FreeCashFlow"] = safe_get(cashflow, "Free Cash Flow").ffill() / Scale
  df["BeginningCash"] = safe_get(cashflow, "Beginning Cash Position").ffill() / Scale
  df["EndingCash"] = safe_get(cashflow, "End Cash Position").ffill() / Scale
  df["FX"] = safe_get(cashflow, "Effect Of Exchange Rate Changes").ffill() / Scale
  df["ChangeInCash"] = safe_get(cashflow, "Changes In Cash").fillna(
      df["OperatingCashFlow"]
      + df["InvestingCashFlow"]
      + df["FinancingCashFlow"]
      + df["FX"]
  ) / Scale

  #Balance Sheet
	#Assets
  df["TotalAssets"] = safe_get(balance, "Total Assets").ffill() / Scale
  df["OtherNonCurrentAssets"] = safe_get(balance, "Other Non Current Assets").ffill() / Scale
  df["InvestmentsAndAdvances"] = safe_get(balance, "Investments And Advances").ffill() / Scale
	
	#Liabilities
  df["TotalLiabilities"] = safe_get(balance, "Total Liabilities Net Minority Interest").ffill() / Scale
  df["NonCurrentDeferredLiabilities"] = safe_get(balance, "Non Current Deferred Liabilities").ffill() / Scale
  df["OtherNonCurrentLiabilities"] = safe_get(balance, "Other Non Current Liabilities").ffill() / Scale

  #Debt Schedule
  df["EBITDA"] = safe_get(income, "EBITDA").ffill() / Scale
  df["TotalDebt"] = safe_get(balance, "Total Debt").ffill() / Scale
  df["LongTermDebt"] = safe_get(balance, "Long Term Debt").ffill() / Scale
  df["ShortTermDebt"] = safe_get(balance, "Current Debt").fillna(0) / Scale
  df["Interest"] = safe_get(income, "Interest Expense").ffill() / Scale
  df["DebtIssued"] = safe_get(cashflow, "Long Term Debt Issuance").fillna(0) / Scale
  df["Repayment"] = safe_get(cashflow, "Long Term Debt Payments").fillna(0) / Scale

  #Equity Schedule
  df["Equity"] = safe_get(balance, "Stockholders Equity").ffill() / Scale
  df["Dividends"] = safe_get(cashflow, "Cash Dividends Paid").ffill() / Scale
  df["SBC"] = safe_get(cashflow, "Stock Based Compensation").ffill() / Scale
  df["ShareIssued"] = safe_get(cashflow, "Proceeds From Stock Option Exercised").ffill() / Scale
  df["BuyBacks"] = safe_get(cashflow, "Repurchase Of Capital Stock").ffill() / Scale
  df["CommonStockEquity"] = safe_get(balance, "Common Stock Equity").ffill() / Scale
  df["PreferredStockEquity"] = safe_get(balance, "Preferred Stock Equity").ffill() / Scale

  #PPE Schedule
  df["PPE"] = safe_get(balance, "Net PPE").ffill() / Scale
  df["Depreciation"] = safe_get(cashflow, "Depreciation").ffill() / Scale
  df["Capex"] = safe_get(cashflow, "Capital Expenditure").ffill() / Scale

  #Working Capital Schedule
	#Current Assets
  df["CurrentAssets"] = safe_get(balance, "Current Assets").ffill() / Scale
  df["CashAndCashEquivalents"] = safe_get(balance, "Cash And Cash Equivalents").ffill() / Scale
  df["OtherShortTermInvestments"] = safe_get(balance, "Other Short Term Investments").ffill() / Scale
  df["Receivables"] = safe_get(balance, "Receivables").ffill() / Scale
  df["RestrictedCash"] = safe_get(balance, "Restricted Cash").ffill() / Scale
  df["OtherCurrentAssets"] = safe_get(balance, "Other Current Assets").ffill() / Scale
	
	#Current Liabilities
  df["CurrentLiabilities"] = safe_get(balance, "Current Liabilities").ffill() / Scale
  df["PayablesAndAccruedExpenses"] = safe_get(balance, "Payables And Accrued Expenses").ffill() / Scale
  df["Pension"] = safe_get(balance, "Pensionand Other Post Retirement Benefit Plans Current").ffill() / Scale
  df["OtherCurrentLiabilities"] = safe_get(balance, "Other Current Liabilities").ffill() / Scale

  df["WorkingCapital"] = safe_get(balance, "Working Capital").ffill() / Scale
  df["NetDebt"] = safe_get(balance, "Net Debt").ffill() / Scale

  #Revenue Drivers
	# Payment Volume & Transactions sourced manually from Visa Investor Reports
	# as this data is not available via yfinance API
  driver_data = pd.DataFrame({
      "Year": df.index,
      "Transactions": [1920000, 2126000, 2338000, 2575000][:len(df)],
      "PaymentVolume": [11600000, 12300000, 13200000, 14200000][:len(df)]
  }).set_index("Year")

  df = df.join(driver_data)
  df = df.round(0)
	
  #Closing Prices
  september_prices = price_data[price_data.index.month == 9]["Close"]
  sept_closing = september_prices.groupby(september_prices.index.year).last()

  df["Closing"] = sept_closing.reindex(df.index.year).values

  #EPS
  df["PreferredStockDividend"] = safe_get(income, "Otherunder Preferred Stock Dividend").ffill() / Scale
  df["NetIncomeCommon"] = safe_get(income, "Net Income Common Stockholders").fillna(
      df["NetIncome"] - df["PreferredStockDividend"]
  ) / Scale
  df["Shares"] = safe_get(balance, "Ordinary Shares Number").ffill()
  df["EPS"] = safe_get(income, "Diluted EPS").fillna(df["NetIncomeCommon"] / df["Shares"])


  df.index = pd.to_datetime(df.index)
  df["Year"] = df.index.year
  df.set_index("Year", inplace=True)

  return df
