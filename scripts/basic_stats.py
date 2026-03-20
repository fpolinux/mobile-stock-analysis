import argparse
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

##Helper function for large fundamentals data
def format_large_number(n):
    if n is None: return "N/A"
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(n) < 1000.0:
            return f"${n:,.2f}{unit}"
        n /= 1000.0
    return f"${n:,.2f}P"

def download_data(ticker):
    data = yf.download(ticker, start= datetime.date.today() - relativedelta(years=1), end=datetime.date.today(), auto_adjust = True)
    return data["Close"]

def run_basic_stats(ticker: str) -> str:
    ticker = ticker.upper().strip()
    if not ticker:
        raise ValueError("Ticker is required")
    ## Download Data
    data = download_data(ticker)
    ## Calculate annualised returns and std dev
    returns = np.log(data/data.shift(1)).dropna()
    mu = (returns.mean()*251).item()
    std_dev = (returns.std()*(251**0.5)).item()
    rf = 0.041
    sharpe = (mu - rf)/std_dev
    info = {"Ticker": f"{ticker}", "Annualised Return": f"{mu:.2%}", "Annualised std dev": f"{std_dev:.2%}", "Sharpe": f"{sharpe:.2}", "Assumed rf": rf}
    return info

def run_kpis(ticker: str) -> str:
    ticker = ticker.upper().strip()
    if not ticker:
        raise ValueError("Ticker is required")
    data = yf.Ticker(ticker)
    kpis = {
        "Ticker": ticker,
        "Trailing PE": round(data.info.get("trailingPE"), 2),
        "Forward PE": round(data.info["forwardPE"], 2),
        "Mkt Cap": format_large_number(data.info["marketCap"]),
        "Trailing EPS": round(data.info.get("trailingEps"), 2),
        "Forward EPS": round(data.info.get("forwardEps"), 2),
        "D/E": round(data.info.get("debtToEquity"), 2),
        "ROE": round(data.info['returnOnEquity'], 2),
        "EBIT Margin": round(data.info.get('operatingMargins'), 2)
    }
    return kpis
