"""Streamlit UI to lookup mutual fund NAV by ISIN using fetch_navs."""

from pathlib import Path
import sys

import streamlit as st

# Ensure project root is on sys.path when launched via `streamlit run`
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ingestion.mutual_funds_api import MutualFund, fetch_navs

@st.cache_data
def load_navs() -> dict[str, MutualFund]:
    """Fetch and cache NAV data once per session."""
    return fetch_navs()

def main() -> None:
    st.title("Mutual Fund ISIN Lookup")
    st.caption(
        "Enter an ISIN to see the scheme name, NAV, and date. "
    )

    navs = load_navs()

    isin_input = st.text_input("ISIN").strip()
    if not isin_input:
        st.info("Type an ISIN to search.")
        return

    if isin_input in navs:
        results = navs[isin_input]
    else:
        st.warning("No scheme found for that ISIN.")
        return

    st.subheader(results.scheme_name)
    st.write(f"NAV: {results.nav}")
    st.write(f"Date: {results.date}")
    st.divider()

if __name__ == "__main__":
    main()
