# BMW Business Analysis — Project Explained

**Your study guide to understanding every file, every concept, and every number**

---

## Part 1: What Are We Actually Doing Here?

### The Real-World Situation

You're a junior analyst at a European long/short equity fund. Your PM has handed you a brief: "Build the investment case on BMW. We already own VW, which is painful. Is BMW better quality? And at what price does it become interesting?"

The P2 project (German Auto Industry Deep-Dive) told you the industry story: two-sided squeeze, China erosion, EV costs. But industry analysis doesn't tell you which *specific company* is worth buying. That's what P4 is for.

**The core question:** Does BMW's structural quality justify its current depressed valuation — or is the market right to be skeptical?

### What "Business Analysis" Means in Practice

A company-level business analysis (sometimes called a "fundamental analysis" or "business teardown") answers five questions:

1. **How does the company make money?** — Revenue model, segments
2. **Where does it make money?** — Geographic exposure  
3. **How efficiently does it make money?** — Margins by segment
4. **What protects its ability to keep making money?** — Competitive moat
5. **What could go wrong?** — Risks that could break the thesis

This project answers all five for BMW, then hands the baton to P5 (3-Statement Model) which builds the financial forecast.

---

## Part 2: Every File Explained

### `bmw_data.py` — The Data Layer

**What it does:** Two jobs: (1) pulls live BMW market data from yfinance, (2) loads hand-curated annual report data from CSVs.

**Key functions:**

`fetch_bmw_snapshot()` — Calls yfinance for BMW.DE and returns ~15 metrics in a flat dict. Everything in here is TTM (trailing twelve months) — meaning the last 12 months of data, not a specific fiscal year. This is what analysts mean when they say "TTM P/E" — it uses the most recent available earnings, not a year-end snapshot.

Why a flat dict and not a DataFrame? Because it's a single company, single point in time. A DataFrame would be like using a spreadsheet to store one number — overkill.

`load_segments()` — Reads `bmw_segments.csv`. Returns a DataFrame with Segment, Year, Revenue, EBIT, and EBIT Margin. This came from BMW's annual reports where they break out results by business unit. You could not get this from yfinance — it only gives you group totals.

`load_geography()` — Reads `bmw_geography.csv`. Regional revenue split. BMW discloses this in the "Revenue by region" table in their annual report appendix.

`load_deliveries()` — Reads `bmw_deliveries.csv`. Vehicle deliveries by powertrain type. BMW reports this in their "Sales" section of the annual report and in monthly press releases.

**`BASE_YEAR = 2025` and `DATA_AS_OF`:** The same vintage system from P2. CSVs are anchored to FY2025. Market data is TTM stamped with today's date. When you write the equity research report (P9), you'll always label which data you're using.

---

### `data/bmw_segments.csv` — Three Business Units

BMW Group has exactly three reportable segments:

**1. Automotive** — The car business. Revenue from selling BMW, MINI, and Rolls-Royce vehicles + after-sales (spare parts, accessories, service contracts). This segment carries all the EV transition cost. When analysts worry about BMW's margins, they mean this segment.

**2. Financial Services** — BMW Bank + BMW Insurance + leasing and financing products. When a customer buys a BMW on finance (most do), the profit on that loan goes here. Why is this important? Because it's structurally high-margin (~7% EBIT), growing, and largely insulated from EV transition costs. It's also a competitive moat — BMW controls the customer from the moment they sign the purchase agreement.

**3. Motorcycles (BMW Motorrad)** — BMW's motorcycle division. Small (~2% of group revenue) but actually the highest-margin segment (~14% EBIT margin). Motorcycles have better pricing power and less EV pressure than cars. It's a self-funding cash generator that most analysts ignore.

**Column guide:**
- `Revenue_Bn_EUR` — total billings before group eliminations
- `EBIT_Bn_EUR` — Earnings Before Interest and Tax
- `EBIT_Margin_Pct` — EBIT / Revenue × 100

**Why EBIT and not EBITDA here?** For segment analysis, EBIT is preferred because each segment has its own depreciation (capex on factories, equipment, tooling). EBITDA would hide the fact that the Automotive segment is spending heavily on EV tooling (D&A going up), which is a real cost.

---

### `data/bmw_geography.csv` — Where The Money Comes From

**Why geography matters for BMW specifically:** China was BMW's profit engine from roughly 2015-2022. High-spec models sold at full price to Chinese premium buyers with minimal discounting. That era is ending. BYD, Huawei's Aito brand, and Li Auto are taking luxury market share in China at a pace nobody predicted.

**Column guide:**
- `Region` — Germany, Rest_of_Europe, North_America, China, RoW
- `Revenue_Pct` — that region's share of Automotive segment revenue

**What to look for in Chart 2:** China peaked at ~21.4% in FY2022 and declined to 19.2% in FY2025. North America has held steady at ~24-25%. This is actually the bull case narrative — BMW is not *fully* dependent on China like VW, and North America is a structural offset.

---

### `data/bmw_deliveries.csv` — The EV Transition in Numbers

**Why this matters:** Investors will re-rate BMW when BEV margins approach ICE margins. That inflection requires scale (more BEV deliveries = better unit economics) and platform efficiency (Neue Klasse). This CSV lets you track the progress.

**Column guide:**
- `Total_000` — total BMW Group deliveries in thousands
- `BEV_000` — battery electric only
- `PHEV_000` — plug-in hybrid (has both battery and combustion engine)
- `ICE_000` — traditional combustion engine only
- `BEV_Pct` — BEV as % of total

**Why BMW's 20.6% BEV mix is significant:** The EU 2035 mandate trajectory (from P2) suggested ~17% by 2025. BMW is *ahead* of the regulatory requirement. VW is behind at ~10%. This matters because falling behind the trajectory means regulatory fine risk — ahead means optionality.

**PHEV declining intentionally:** BMW is phasing out PHEVs in favour of pure BEV. PHEVs were a transition product (offered EV subsidies while using ICE as range backup). As BEV range improves, PHEVs become redundant.

---

### `charts.py` — Four Visualisations

**Chart 1: `plot_segment_performance()`**
Uses `make_subplots(secondary_y=True)` — a dual-axis chart. Left y-axis is revenue (stacked bars by segment). Right y-axis is Automotive EBIT margin % (dotted black line).

Why dual axis? Revenue and margin are different scales (billions vs percentage). Without a secondary axis, the margin line would be invisible next to €100bn+ bars.

The "stack" in `barmode="stack"` tells Plotly to pile the bars on top of each other rather than side by side — good for showing total group revenue AND segment composition simultaneously.

**Chart 2: `plot_geographic_mix()`**
100% stacked bar chart (every year sums to ~100%). Lets you see the *shift* in mix even as absolute revenue changes. China's red bar visually shrinking year-by-year tells the story instantly.

Annotations added in the China bars to show exact % — because China is the key risk metric, analysts want to see the number clearly without having to hover.

**Chart 3: `plot_powertrain_transition()`**
Stacked bars (ICE at bottom, PHEV in middle, BEV on top) plus BEV mix % as a dotted line on secondary axis. ICE is grey (commodity/declining), PHEV is green (transition), BEV is BMW blue (the future).

The visual story: ICE bars shrinking, BEV bars growing, dotted line accelerating upward.

**Chart 4: `plot_moat_radar()`**
A radar (spider) chart — each axis is a competitive dimension, the polygon area represents overall competitive strength. BMW's polygon should be the largest.

Six dimensions chosen:
1. Brand Premium — pricing power above commodity cars
2. EV Readiness — technology + BEV mix progress
3. China Exposure Risk — inverted (lower exposure = higher score here)
4. Financial Services — captive finance moat
5. Margin Resilience — ability to hold margins under pressure
6. Neue Klasse / Pipeline — quality of future product roadmap

`go.Scatterpolar` is Plotly's radar chart type. `fill="toself"` fills the polygon. `opacity=0.15` makes the fill semi-transparent so overlapping polygons are visible.

---

### `analysis.py` — The Runner

Calls everything in sequence, does a data vintage check (same pattern as P2), and prints a structured terminal summary. The terminal output is designed to be readable on its own — like a Bloomberg terminal function summary.

The `min(..., 1.0) * 100` in the dividend yield calculation catches a yfinance bug where `dividendYield` is sometimes returned as a float like `6.48` (meaning 6.48%) instead of `0.0648`. Capping at 100% catches the error.

---

## Part 3: Core Financial Concepts

### Captive Finance and Why It Changes Everything

Most people think of BMW as a car company. It is also a bank. BMW Financial Services had a loan book of approximately €140bn in FY2025 — larger than many mid-sized European banks.

This matters for three reasons:

**1. It inflates "net debt."** When yfinance shows BMW's net debt at ~€96bn, that includes all the car loans BMW Bank has made. These are matched liabilities (BMW borrows money at 3%, lends to car buyers at 6%, earns the spread). This is not industrial leverage — it's banking leverage, which is normal and self-funding. BMW's *industrial* net cash position (stripping out financial services) is actually positive.

In an equity research report you would always present two net debt figures: group (includes FinServ) and industrial (strips it out). Analysts value the automotive business separately from the financial services business.

**2. It creates a recurring revenue stream.** When BMW sells you a car on a 4-year lease, they get margin on the car sale AND four years of financing income AND they get the car back at end of lease to resell as certified pre-owned. Three bites of the same apple.

**3. It deepens customer loyalty.** A customer financing through BMW Financial Services is more likely to buy another BMW at end of contract. The finance arm is a retention mechanism, not just a profit centre.

### EBIT vs EBITDA — When to Use Each

**EBIT** (Earnings Before Interest and Tax) = Revenue − COGS − Operating Expenses

**EBITDA** = EBIT + Depreciation + Amortisation

For BMW's *segment analysis*, use EBIT. Each segment has real, segment-specific capex (automotive has factories and tooling; financial services has IT systems; motorcycles has engine plants). The depreciation on that capex is a real ongoing cost of doing business in that segment, so EBIT captures it.

For *valuation* (EV/EBITDA multiples), use EBITDA. When comparing BMW's EV/EBITDA to Stellantis or Renault, you want to strip out depreciation so that OEMs with different investment cycles (e.g., one in heavy capex phase for EVs, one coasting on old ICE tooling) are comparable. It's not perfect, but it's the market standard.

### Neue Klasse — Why Analysts Care

BMW's current BEV lineup (iX, i4, iX3, i5) is built on platforms shared with ICE cars. This means compromises: battery packaging is constrained, software architecture is carried over from ICE, and manufacturing can't be fully optimised for BEV.

Neue Klasse is a clean-sheet BEV platform. Like VW's MEB, but BMW claims it goes further in battery chemistry (round cell format, higher energy density), software (BMW OS 9, over-the-air updates), and manufacturing (new Debrecen, Hungary plant).

The investment thesis implication: once Neue Klasse launches at scale (2026-2028), BMW's BEV unit margin should close most of the gap to ICE margins. Today the market is pricing BMW as if that never happens. If it does — and BMW's engineering track record suggests it will — the stock re-rates.

---

## Part 4: Interview Scripts

### "Walk me through BMW's business model"

"BMW Group is a premium automotive manufacturer with three segments: Automotive, Financial Services, and Motorcycles. The automotive segment — BMW, MINI, and Rolls-Royce — generates about 70% of group revenue and is the segment facing EV transition pressure. Financial Services, which is BMW Bank plus leasing, contributes about 29% of revenue and acts as a high-margin stabiliser at around 7% EBIT margin. Motorcycles is small but actually the highest-margin segment at 14%.

Geographically, BMW earns roughly a quarter from North America, a third from rest of Europe, 19% from China — which has been declining since the FY2022 peak — and the balance from Germany and the rest of the world.

On EV transition, BMW is the most advanced of the German OEMs at 20.6% BEV mix in FY2025, and its Neue Klasse platform launching in 2026 is expected to bring BEV margins closer to ICE margins — which is the key re-rating catalyst."

### "What's BMW's competitive moat?"

"I'd identify three structural advantages. First, brand — BMW's premium positioning allows it to price above commodity OEMs with lower volume sensitivity. The average selling price is around €55k versus €28k for VW Group, which means margin can hold even on lower volumes.

Second, financial services — BMW Bank is a genuine moat. Customers financing through BMW are more likely to return, BMW earns the financing spread, and at end of lease they get the used car back for certified pre-owned sale. It's recurring revenue attached to the car sale.

Third, the Neue Klasse pipeline. It's a clean-sheet BEV architecture that BMW claims will reduce costs 25-30% versus current BEV models and improve software quality significantly. If it delivers, it closes the margin gap between BEV and ICE — which is currently the biggest concern for automotive investors."

---

## Part 5: What Comes Next

This project answers the *business* questions. The next layer is the *financial model*:

- **P5: 3-Statement Model** — Build BMW's income statement, balance sheet, and cash flow statement in Python/Excel. Project FY2026E-FY2028E based on the thesis built here.
- **P7: DCF** — Value BMW using discounted cash flow. The Neue Klasse scenario will be your upside case; China continued erosion will be your downside.
- **P9: Full Equity Research Report** — Combine P2 (industry), P4 (business), P5 (model), and P7 (DCF) into a professional 20-25 page report with a price target and investment recommendation.

Everything you've learned in this project feeds directly into those. The segment margins you've studied become your income statement assumptions. The geographic exposure becomes your sensitivity analysis. The Neue Klasse thesis becomes your upside scenario narrative.
