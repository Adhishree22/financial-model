
import yfinance as yf
import pandas as pd

def get_financial_statements(ticker, periods=5):
  
  stock = yf.Ticker(ticker)

  income = stock.financials.T.sort_index().iloc[:periods]
  balance = stock.balance_sheet.T.sort_index().iloc[:periods]
  cashflow = stock.cashflow.T.sort_index().iloc[:periods]

  return {
      "income": income,
      "balance": balance,
      "cashflow": cashflow
  }

def get_beta(ticker):
  
  stock = yf.Ticker(ticker)

  beta = stock.info.get("beta", None)

  # fallback if beta not available
  if beta is None:
    beta = 1.0

  return beta

def get_price_data(ticker, income_index):
  
  start_year = income_index.year.min()
  end_year = income_index.year.max()

  price_data = yf.download(
      ticker,
      start=f"{start_year}-01-01",
      end=f"{end_year}-12-31",
      progress=False,
      auto_adjust=True
  )

  price_data = price_data.set_axis(
      price_data.columns.droplevel(1), axis=1
  ).reset_index()
  price_data.index = pd.to_datetime(price_data.index)
  price_data["Date"] = pd.to_datetime(price_data["Date"])
  price_data = price_data.set_index("Date")

  return price_data


def inspect_columns(data_dict, price_data):
  
  column_names = {
      "Income Statement": data_dict["income"],
      "Balance Sheet": data_dict["balance"],
      "Cashflow Statement": data_dict["cashflow"],
      "Price Data": price_data
      }

  for name, df in column_names.items():
    print(f"{name} Columns:\n{df.columns}\n")
