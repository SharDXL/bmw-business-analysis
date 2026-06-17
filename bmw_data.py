"""
bmw_data.py
-----------
Data layer for the BMW Business Analysis project.

Live data: yfinance (BMW.DE) for current market snapshot
Static data: hand-curated CSVs from BMW Group Annual Reports 2021-2025
  - bmw_segments.csv   : Revenue + EBIT by segment (Automotive / FinServ / Motorcycles)
  - bmw_geography.csv  : Revenue breakdown by region
  - bmw_deliveries.csv : Vehicle deliveries by powertrain (BEV / PHEV / ICE)

Data vintage:
  BASE_YEAR      = FY2025 (most recent complete fiscal year)
  DATA_AS_OF     = today (for live market prices / TTM multiples)
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime

BASE_YEAR  = 2025
DATA_AS_OF = datetime.today().strftime("%d %b %Y")
TICKER     = "BMW.DE"
DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")


def fetch_bmw_snapshot() -> dict:
    """
    Pull live market + TTM financials for BMW via yfinance.
    Returns a flat dict of key metrics.
    """
    t    = yf.Ticker(TICKER)
    info = t.info
    snap = {
        "ticker":           TICKER,
        "price":            round(info.get("currentPrice", 0), 2),
        "market_cap_bn":    round(info.get("marketCap", 0) / 1e9, 1),
        "revenue_bn":       round(info.get("totalRevenue", 0) / 1e9, 1),
        "ebitda_bn":        round(info.get("ebitda", 0) / 1e9, 1),
        "net_income_bn":    round(info.get("netIncomeToCommon", 0) / 1e9, 1),
        "total_debt_bn":    round(info.get("totalDebt", 0) / 1e9, 1),
        "cash_bn":          round(info.get("totalCash", 0) / 1e9, 1),
        "net_debt_bn":      round((info.get("totalDebt", 0) - info.get("totalCash", 0)) / 1e9, 1),
        "pe_ratio":         round(info.get("trailingPE", 0), 1),
        "ev_ebitda":        round(info.get("enterpriseToEbitda", 0), 1),
        "ev_revenue":       round(info.get("enterpriseToRevenue", 0), 1),
        "op_margin_pct":    round((info.get("operatingMargins", 0) or 0) * 100, 1),
        "roe_pct":          round((info.get("returnOnEquity", 0) or 0) * 100, 1),
        # dividendYield from yfinance is already a ratio (e.g. 0.065 = 6.5%)
        # Sanity cap: if value > 1 it's been returned as a percentage already
        "_raw_div":         info.get("dividendYield", 0) or 0,
        "div_yield_pct":    round(min((info.get("dividendYield", 0) or 0), 1.0) * 100, 2),
        "52w_high":         round(info.get("fiftyTwoWeekHigh", 0), 2),
        "52w_low":          round(info.get("fiftyTwoWeekLow", 0), 2),
        "beta":             round(info.get("beta", 0), 2),
        "data_as_of":       DATA_AS_OF,
    }
    # Enterprise Value
    snap["ev_bn"] = round(snap["market_cap_bn"] + snap["net_debt_bn"], 1)
    return snap


def load_segments() -> pd.DataFrame:
    """Load segment P&L from CSV. Columns: Segment, Year, Revenue_Bn_EUR, EBIT_Bn_EUR, EBIT_Margin_Pct"""
    return pd.read_csv(os.path.join(DATA_DIR, "bmw_segments.csv"))


def load_geography() -> pd.DataFrame:
    """Load geographic revenue from CSV. Columns: Region, Year, Revenue_Bn_EUR, Revenue_Pct"""
    return pd.read_csv(os.path.join(DATA_DIR, "bmw_geography.csv"))


def load_deliveries() -> pd.DataFrame:
    """Load vehicle delivery mix from CSV. Columns: Year, Total_000, BEV_000, PHEV_000, ICE_000, BEV_Pct, PHEV_Pct"""
    return pd.read_csv(os.path.join(DATA_DIR, "bmw_deliveries.csv"))
