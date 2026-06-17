"""
analysis.py
-----------
Main runner for the BMW Business Analysis project.

Usage:
    python analysis.py

Runs in sequence:
  1. Live BMW snapshot (yfinance)
  2. Loads static segment / geography / delivery CSVs
  3. Prints data vintage check
  4. Generates four Plotly charts
  5. Prints BMW investment summary to terminal
"""

import bmw_data as bd
import charts as ch

SEP  = "-" * 60
SEP2 = "=" * 60


def run():
    print(f"\n{SEP2}")
    print("  BMW GROUP BUSINESS ANALYSIS -- Shardul Pundir")
    print("  github.com/SharDXL/bmw-business-analysis")
    print(SEP2)

    # 1. Live snapshot ─────────────────────────────────────────────────────────
    print(f"\n{SEP}\n  1/4  Live Market Snapshot (yfinance)\n{SEP}")
    snap = bd.fetch_bmw_snapshot()

    print(f"\n  BMW.DE  --  as of {snap['data_as_of']}")
    print(f"  {'Price':<22} EUR {snap['price']}")
    print(f"  {'Market Cap':<22} EUR {snap['market_cap_bn']:.1f}bn")
    print(f"  {'Enterprise Value':<22} EUR {snap['ev_bn']:.1f}bn")
    print(f"  {'Net Debt':<22} EUR {snap['net_debt_bn']:.1f}bn")
    print(f"  {'Revenue (TTM)':<22} EUR {snap['revenue_bn']:.1f}bn")
    print(f"  {'EBITDA (TTM)':<22} EUR {snap['ebitda_bn']:.1f}bn")
    print(f"  {'Net Income (TTM)':<22} EUR {snap['net_income_bn']:.1f}bn")
    print(f"  {'EV/EBITDA':<22} {snap['ev_ebitda']}x")
    print(f"  {'P/E':<22} {snap['pe_ratio']}x")
    print(f"  {'Operating Margin':<22} {snap['op_margin_pct']}%")
    print(f"  {'ROE':<22} {snap['roe_pct']}%")
    print(f"  {'Dividend Yield':<22} {snap['div_yield_pct']}%")
    print(f"  {'52W Range':<22} EUR {snap['52w_low']} – {snap['52w_high']}")
    print(f"  {'Beta':<22} {snap['beta']}")

    # 2. Load static data ──────────────────────────────────────────────────────
    print(f"\n{SEP}\n  2/4  Loading static datasets (BMW Annual Reports)\n{SEP}")
    seg_df = bd.load_segments()
    geo_df = bd.load_geography()
    del_df = bd.load_deliveries()
    print(f"  Segment P&L : {seg_df.shape[0]} rows  (FY{seg_df.Year.min()}-FY{seg_df.Year.max()})")
    print(f"  Geography   : {geo_df.shape[0]} rows  (FY{geo_df.Year.min()}-FY{geo_df.Year.max()})")
    print(f"  Deliveries  : {del_df.shape[0]} rows  (FY{del_df.Year.min()}-FY{del_df.Year.max()})")

    # 3. Data vintage check ────────────────────────────────────────────────────
    print(f"\n{SEP}\n  Data Vintage Check\n{SEP}")
    for label, df, year_col in [
        ("Segment P&L", seg_df, "Year"),
        ("Geography",   geo_df, "Year"),
        ("Deliveries",  del_df, "Year"),
    ]:
        years  = sorted(df[year_col].unique())
        status = "OK" if bd.BASE_YEAR in years else f"WARNING: FY{bd.BASE_YEAR} MISSING"
        print(f"  {label:<15} FY{years[0]}-FY{years[-1]}  {status}")
    print(f"\n  Live market data : TTM as of {bd.DATA_AS_OF}")
    print(f"  Static CSVs      : FY{bd.BASE_YEAR} (BMW Annual Report)")
    print(f"  NOTE: multiples above are TTM; static segment data is FY{bd.BASE_YEAR}.")

    # 4. Charts ────────────────────────────────────────────────────────────────
    print(f"\n{SEP}\n  3/4  Generating charts\n{SEP}")
    ch.plot_segment_performance(seg_df)
    ch.plot_geographic_mix(geo_df)
    ch.plot_powertrain_transition(del_df)
    ch.plot_moat_radar()

    # 5. Summary ───────────────────────────────────────────────────────────────
    print(f"\n{SEP}\n  4/4  BMW Investment Summary  (FY{bd.BASE_YEAR})\n{SEP}")

    fy = seg_df[seg_df["Year"] == bd.BASE_YEAR]
    total_rev  = fy["Revenue_Bn_EUR"].sum()
    total_ebit = fy["EBIT_Bn_EUR"].sum()
    group_margin = round(total_ebit / total_rev * 100, 1)

    auto = fy[fy["Segment"] == "Automotive"].iloc[0]

    print(f"\n  Group Revenue (FY{bd.BASE_YEAR})  : EUR {total_rev:.1f}bn")
    print(f"  Group EBIT   (FY{bd.BASE_YEAR})  : EUR {total_ebit:.1f}bn  ({group_margin}%)")
    print(f"  Automotive margin            : {auto['EBIT_Margin_Pct']}%")

    bev_fy = del_df[del_df["Year"] == bd.BASE_YEAR].iloc[0]
    print(f"\n  Deliveries FY{bd.BASE_YEAR}           : {bev_fy['Total_000']:.0f}k vehicles")
    print(f"  BEV mix                      : {bev_fy['BEV_Pct']:.1f}%  ({bev_fy['BEV_000']:.0f}k units)")

    china_fy = geo_df[(geo_df["Region"] == "China") & (geo_df["Year"] == bd.BASE_YEAR)].iloc[0]
    print(f"  China revenue share          : {china_fy['Revenue_Pct']:.1f}%")

    print(f"\n  Valuation (TTM as of {bd.DATA_AS_OF}):")
    print(f"    EV/EBITDA  {snap['ev_ebitda']}x")
    print(f"    P/E        {snap['pe_ratio']}x")
    print(f"    Mkt Cap    EUR {snap['market_cap_bn']:.1f}bn")

    print(f"\n  Key Catalyst : Neue Klasse platform launch (2026-2027)")
    print(f"  Key Risk     : China revenue decline + EV margin compression")
    print(f"  Thesis       : Cheapest quality OEM; Neue Klasse re-rates multiples")

    print(f"\n{SEP}")
    print("  Charts saved to /charts/  (open .html for interactive)")
    print(f"{SEP}\n")


if __name__ == "__main__":
    run()
