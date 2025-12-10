from src.ingestion.mutual_funds_api import fetch_navs

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