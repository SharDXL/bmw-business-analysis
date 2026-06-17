# BMW Group Business Analysis

**Company-level deep-dive into BMW AG — P4 of the German Auto equity research roadmap**

`BMW.DE` | FY2021–FY2025 | Live market data via yfinance

---

## What This Is

A four-chart Python project that analyses BMW Group as a standalone investment — moving from the industry layer (P2: German Auto Deep-Dive) down to the company level. The core question: **is BMW's structural quality (brand, financial services, Neue Klasse pipeline) sufficient to justify a re-rating from today's depressed multiples?**

Project roadmap context:
**P2 Industry Deep-Dive → P4 BMW Business Analysis (this) → P5 3-Statement Model → P7 DCF → P9 Full Equity Research Report**

---

## Four Charts, Four Lenses

| Chart | File | What It Shows |
|---|---|---|
| Segment Performance | `01_segment_performance.html` | Revenue by segment + Automotive EBIT margin trend |
| Geographic Mix | `02_geographic_mix.html` | China dependency declining; North America growing |
| Powertrain Transition | `03_powertrain_transition.html` | BEV/PHEV/ICE delivery volumes + BEV mix % rising |
| Moat Radar | `04_moat_radar.html` | BMW vs Mercedes vs VW on 6 competitive dimensions |

---

## Key Findings (FY2025)

**Business mix:** BMW Group has three segments. Automotive (cars + after-sales) generates ~70% of revenue but carries all the EV transition risk. Financial Services (BMW Bank + leasing) contributes ~29% of revenue and acts as a stable margin cushion — critical context often missed by analysts focused only on the car business.

**Geography:** China peaked at ~21% of revenue in FY2022 and has been declining since. FY2025 China share is ~19.2%, the lowest since FY2019. This is structural, not cyclical — local Chinese brands (BYD, Li Auto, Huawei-backed) have permanently taken share. Management's response is accelerating Neue Klasse in China.

**EV transition:** BMW leads German OEMs at 20.6% BEV mix (FY2025), up from 1.9% in FY2020. The Neue Klasse platform (dedicated BEV architecture, new battery technology, launching 2026) is expected to bring BEV economics closer to ICE margins — the key missing piece in the bull case.

**Valuation:** At P/E 5.6x and EV/EBITDA 9.5x, BMW trades at a near-trough multiple. The implied assumption is that Neue Klasse fails and China erosion continues. Any recovery in either catalyst re-rates the stock.

**Note on Net Debt:** BMW's reported net debt (~€96bn) includes BMW Bank's entire lending book (auto loans, leases). This is standard for OEMs with captive finance arms and not comparable to industrial net debt. Automotive segment net cash is positive — BMW has no funding risk.

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
