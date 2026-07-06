# BMW Group Business Analysis

**Company-level deep-dive into BMW AG**

`BMW.DE` | FY2021–FY2025 | Live market data via yfinance

---

## What This Is

A four-chart Python project that analyses BMW Group as a standalone investment. The core question: **is BMW's structural quality (brand, financial services, Neue Klasse pipeline) sufficient to justify a re-rating from today's depressed multiples?**

---

## Four Charts, Four Lenses

| Chart | File | What It Shows |
|---|---|---|
| Segment Performance | `01_segment_performance.html` | Revenue by segment + Automotive EBIT margin trend |
| Geographic Mix | `02_geographic_mix.html` | China dependency declining; North America growing |
| Powertrain Transition | `03_powertrain_transition.html` | BEV/PHEV/ICE delivery volumes + BEV mix % rising |
| Moat Radar | `04_moat_radar.html` | BMW vs Mercedes vs VW on 6 competitive dimensions |

---

## Key Findings (FY2025 actuals; market data last refreshed 06 July 2026 — updates automatically, see below)

**Business mix:** BMW Group has three segments. Automotive (cars + after-sales) generates the large majority of revenue but carries all the EV transition risk. Financial Services (BMW Bank + leasing) acts as a stable margin cushion — critical context often missed by analysts focused only on the car business.

**Geography:** China revenue share is 18.6% in the latest data, down from its FY2022 peak. This is structural, not cyclical — local Chinese brands (BYD, Li Auto, Huawei-backed) have permanently taken share. Management's response is accelerating Neue Klasse in China.

**EV transition:** BMW leads German OEMs at 17.9% BEV mix (FY2025, 442k units) — this figure now traces to BMW's own annual report rather than an earlier unlabeled estimate. The Neue Klasse platform (dedicated BEV architecture, new battery technology, launching 2026) is expected to bring BEV economics closer to ICE margins — the key missing piece in the bull case.

**FY2025 actuals (corrected — see P3 for the full model):** Group revenue EUR 160.5bn, Group EBIT EUR 8.9bn (5.5% margin), Automotive segment margin 5.3% — below the 8.5% figure an earlier draft of this analysis had assumed for FY2026E. BMW's own FY2026 guidance points to a 4-6% Automotive margin, not the more optimistic recovery this project originally modelled.

**Valuation:** At the latest refresh, BMW trades at EV/EBITDA 9.2x and P/E 5.4x (TTM) — check `charts/01_segment_performance.html` and the live run output for the current snapshot rather than quoting a fixed multiple, since both move with the share price.

**Note on Net Debt:** BMW's reported net debt includes BMW Bank's entire lending book (auto loans, leases). This is standard for OEMs with captive finance arms and not comparable to industrial net debt. Automotive segment net cash is positive — BMW has no funding risk.

---

## Project Structure

```
bmw-business-analysis/
├── analysis.py          # Main runner
├── bmw_data.py          # Data layer — yfinance live + static CSV loaders
├── charts.py            # Four Plotly visualisations
├── requirements.txt
├── data/
│   ├── bmw_segments.csv    # Revenue + EBIT by segment FY2021-2025
│   ├── bmw_geography.csv   # Revenue breakdown by region FY2021-2025
│   └── bmw_deliveries.csv  # Vehicle deliveries by powertrain FY2020-2025
└── charts/              # Output folder — HTML + PNG charts
```

---

## Setup & Run

```bash
git clone https://github.com/SharDXL/bmw-business-analysis
cd bmw-business-analysis
pip install -r requirements.txt
python analysis.py
```

---

## Key Concepts

**Captive Finance Arms** — BMW Financial Services (BMW Bank) provides loans and leases to BMW buyers. This is extremely high-margin (~7% EBIT margin) and acts as a moat — BMW controls the entire customer relationship from sale to financing to service. Mercedes and VW have the same structure. When comparing BMW's net debt to, say, Apple's, the financial services debt is not industrial leverage.

**Neue Klasse** — BMW's next-generation BEV platform. Unlike the current approach (BEV and ICE sharing the same platform), Neue Klasse is BEV-native, meaning optimized battery packaging, software architecture, and manufacturing. Expected to reduce BEV cost by 25-30% vs current models. The iX3 built on Neue Klasse launches in 2026.

**Automotive EBIT Margin** — The segment-level metric that matters most. BMW's 6.6% automotive margin in FY2025 is significantly better than VW (~3%) but below its own 8.7% peak in FY2022. Recovery to 7-8% requires Neue Klasse cost efficiency + China stabilisation.

**Average Selling Price (ASP)** — BMW's ASP is ~€55k vs VW Group's ~€28k. Premium positioning means lower volume sensitivity and higher pricing power, which is why BMW can tolerate China market share loss better than VW.

---

*Data: BMW Group Annual Reports 2021-2025 (static CSVs), Yahoo Finance (live TTM). For educational purposes.*
