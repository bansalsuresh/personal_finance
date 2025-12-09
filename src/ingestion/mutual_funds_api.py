"""
https://portal.amfiindia.com/spages/NAVAll.txt
Search "Mutual Fund NAV" on RapidAPI
https://api.mfapi.in/mf/119551

Scheme Code;ISIN Div Payout/ ISIN Growth;ISIN Div Reinvestment;Scheme Name;Net Asset Value;Date
Open Ended Schemes(Debt Scheme - Banking and PSU Fund)
Aditya Birla Sun Life Mutual Fund
119551;INF209KA12Z1;INF209KA13Z9;Aditya Birla Sun Life Banking & PSU Debt Fund  - DIRECT - IDCW;110.3373;05-Dec-2025
119552;INF209K01YM2;-;Aditya Birla Sun Life Banking & PSU Debt Fund  - DIRECT - MONTHLY IDCW;117.6559;05-Dec-2025
"""

import requests
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from config.mutual_fund import URL, LOCAL_COPY

@dataclass
class MutualFund:
    scheme_code: str
    isin1: str
    isin2: str
    scheme_name: str
    nav: float
    date: date

def fetch_navs(url: str = URL) -> dict[str, MutualFund]:
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        print(f"Connected to amfi india")
        text = resp.text
    except Exception as exc:
        if LOCAL_COPY.exists():
            text = LOCAL_COPY.read_text(encoding="utf-8")
            print(f"Using local NAV copy due to download error: {exc}")
        else:
            raise
    lines = text.splitlines()
    if not lines:
        raise ValueError("Empty response from NAV feed")
    # skip header
    entries: dict[str, MutualFund] = {}
    for line in lines[1:]:
        parts = line.split(";")
        if len(parts) < 6:
            continue  # skip malformed lines
        scheme_code, isin1, isin2, scheme_name, nav, date = parts[:6]
        mf = MutualFund(
            scheme_code=scheme_code.strip(),
            isin1=isin1.strip(),
            isin2=isin2.strip(),
            scheme_name=scheme_name.strip(),
            nav=nav.strip(),
            date=date.strip(),
        )
        if mf.isin1:  # ensure key present
            entries[mf.isin1] = mf
    return entries

def main():
    try:
        navs = fetch_navs()
    except Exception as exc:
        print(f"Failed to load NAV data: {exc}")
        return

    isin = input("Enter ISIN: ").strip()
    fund = navs.get(isin)
    if fund:
        print(f"NAV for {fund.scheme_name} ({fund.isin1}) as of {fund.date}: {fund.nav}")
    else:
        print("ISIN not found.")

if __name__ == "__main__":
    main()

