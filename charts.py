"""
charts.py
---------
Four Plotly charts for the BMW Business Analysis project.

Chart 1 - Segment Revenue & Margin  : Stacked bar (revenue) + line (EBIT margin %)
Chart 2 - Geographic Mix            : 100% stacked bar showing regional revenue shift
Chart 3 - Powertrain Transition     : Stacked area BEV / PHEV / ICE delivery volumes
Chart 4 - BMW Moat Scorecard        : Radar chart of qualitative competitive dimensions
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Colour palette
COLOURS = {
    "Automotive":         "#1A56DB",
    "Financial_Services": "#0E9F6E",
    "Motorcycles":        "#D97706",
    "Germany":            "#6B7280",
    "Rest_of_Europe":     "#3B82F6",
    "North_America":      "#10B981",
    "China":              "#EF4444",
    "RoW":                "#8B5CF6",
    "BEV":                "#1A56DB",
    "PHEV":               "#0E9F6E",
    "ICE":                "#9CA3AF",
}


def _save(fig, name: str) -> str:
    path = os.path.join(CHARTS_DIR, name)
    fig.write_html(path)
    try:
        fig.write_image(path.replace(".html", ".png"), scale=2)
    except Exception:
        pass
    print(f"  OK {name}")
    return path


# ── Chart 1: Segment Revenue (bars) + EBIT Margin (line) ─────────────────────

def plot_segment_performance(seg_df: pd.DataFrame) -> str:
    years = sorted(seg_df["Year"].unique())
    segments = ["Automotive", "Financial_Services", "Motorcycles"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for seg in segments:
        subset = seg_df[seg_df["Segment"] == seg].sort_values("Year")
        label  = seg.replace("_", " ")
        fig.add_trace(go.Bar(
            x=subset["Year"], y=subset["Revenue_Bn_EUR"],
            name=label, marker_color=COLOURS[seg],
            hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>Revenue: €%{{y:.1f}}bn<extra></extra>",
        ), secondary_y=False)

    # EBIT margin for Automotive on secondary axis (most meaningful margin)
    auto = seg_df[seg_df["Segment"] == "Automotive"].sort_values("Year")
    fig.add_trace(go.Scatter(
        x=auto["Year"], y=auto["EBIT_Margin_Pct"],
        name="Auto EBIT Margin %",
        mode="lines+markers",
        line=dict(color="#111827", width=2.5, dash="dot"),
        marker=dict(size=8),
        hovertemplate="Automotive EBIT Margin: %{y:.1f}%<extra></extra>",
    ), secondary_y=True)

    fig.update_layout(
        title=dict(
            text="<b>BMW Group — Segment Revenue & Automotive EBIT Margin</b><br>"
                 "<sup>FY2021–FY2025 | Automotive dominates revenue; Financial Services is high-margin stabiliser</sup>",
            x=0.5, font=dict(size=15)),
        barmode="stack",
        xaxis=dict(title="Fiscal Year", dtick=1),
        yaxis=dict(title="Revenue (€bn)", showgrid=True, gridcolor="#F3F4F6"),
        yaxis2=dict(title="EBIT Margin (%)", ticksuffix="%", showgrid=False, range=[0, 15]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white", paper_bgcolor="white",
        height=500, margin=dict(l=60, r=60, t=90, b=60),
    )
    return _save(fig, "01_segment_performance.html")


# ── Chart 2: Geographic Revenue Mix ──────────────────────────────────────────

def plot_geographic_mix(geo_df: pd.DataFrame) -> str:
    years    = sorted(geo_df["Year"].unique())
    regions  = ["China", "North_America", "Rest_of_Europe", "Germany", "RoW"]

    fig = go.Figure()
    for region in regions:
        subset = geo_df[geo_df["Region"] == region].sort_values("Year")
        label  = region.replace("_", " ")
        fig.add_trace(go.Bar(
            x=subset["Year"], y=subset["Revenue_Pct"],
            name=label, marker_color=COLOURS[region],
            hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>Revenue share: %{{y:.1f}}%<extra></extra>",
        ))

    # Annotate China trend
    china = geo_df[geo_df["Region"] == "China"].sort_values("Year")
    for _, row in china.iterrows():
        fig.add_annotation(
            x=row["Year"], y=row["Revenue_Pct"] / 2,
            text=f"{row['Revenue_Pct']:.1f}%",
            showarrow=False, font=dict(size=9, color="white"),
        )

    fig.update_layout(
        title=dict(
            text="<b>BMW Group — Revenue by Geography (%)</b><br>"
                 "<sup>FY2021–FY2025 | China peak 2022; structural decline since</sup>",
            x=0.5, font=dict(size=15)),
        barmode="stack",
        xaxis=dict(title="Fiscal Year", dtick=1),
        yaxis=dict(title="Revenue Share (%)", ticksuffix="%", range=[0, 101]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white", paper_bgcolor="white",
        height=480, margin=dict(l=60, r=40, t=90, b=60),
    )
    return _save(fig, "02_geographic_mix.html")


# ── Chart 3: Powertrain Transition ────────────────────────────────────────────

def plot_powertrain_transition(del_df: pd.DataFrame) -> str:
    fig = go.Figure()

    for col, label, colour in [
        ("ICE_000",  "ICE",  COLOURS["ICE"]),
        ("PHEV_000", "PHEV", COLOURS["PHEV"]),
        ("BEV_000",  "BEV",  COLOURS["BEV"]),
    ]:
        fig.add_trace(go.Bar(
            x=del_df["Year"], y=del_df[col],
            name=label, marker_color=colour,
            hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>Deliveries: %{{y:.0f}}k<extra></extra>",
        ))

    # BEV % line on secondary axis
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    for col, label, colour in [
        ("ICE_000",  "ICE",  COLOURS["ICE"]),
        ("PHEV_000", "PHEV", COLOURS["PHEV"]),
        ("BEV_000",  "BEV",  COLOURS["BEV"]),
    ]:
        fig2.add_trace(go.Bar(
            x=del_df["Year"], y=del_df[col],
            name=label, marker_color=colour,
            hovertemplate=f"<b>{label}</b><br>%{{x}}: %{{y:.0f}}k<extra></extra>",
        ), secondary_y=False)

    fig2.add_trace(go.Scatter(
        x=del_df["Year"], y=del_df["BEV_Pct"],
        name="BEV Mix %",
        mode="lines+markers",
        line=dict(color="#111827", width=2.5, dash="dot"),
        marker=dict(size=8),
        hovertemplate="BEV Mix: %{y:.1f}%<extra></extra>",
    ), secondary_y=True)

    fig2.update_layout(
        title=dict(
            text="<b>BMW Group — Powertrain Transition</b><br>"
                 "<sup>FY2020–FY2025 | BEV deliveries and mix % rising; Neue Klasse platform targets acceleration</sup>",
            x=0.5, font=dict(size=15)),
        barmode="stack",
        xaxis=dict(title="Year", dtick=1),
        yaxis=dict(title="Deliveries (thousands)", showgrid=True, gridcolor="#F3F4F6"),
        yaxis2=dict(title="BEV Mix (%)", ticksuffix="%", range=[0, 40], showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white", paper_bgcolor="white",
        height=480, margin=dict(l=60, r=60, t=90, b=60),
    )
    return _save(fig2, "03_powertrain_transition.html")


# ── Chart 4: Competitive Moat Radar ──────────────────────────────────────────

def plot_moat_radar() -> str:
    """
    Qualitative moat scorecard: BMW vs Mercedes vs VW on 6 dimensions.
    Scores are analyst-assigned (1-10) based on public information.
    """
    categories = [
        "Brand Premium",
        "EV Readiness",
        "China Exposure Risk",   # lower = better (inverted)
        "Financial Services",
        "Margin Resilience",
        "Neue Klasse / Pipeline",
    ]

    # Scores out of 10 (higher = better, except China Exposure Risk which is inverted)
    oems = {
        "BMW":      [9, 8, 6, 9, 7, 9],
        "Mercedes": [9, 6, 6, 8, 7, 6],
        "VW":       [6, 5, 4, 5, 4, 6],
    }
    colours = {"BMW": "#1A56DB", "Mercedes": "#111827", "VW": "#059669"}

    fig = go.Figure()
    cats_closed = categories + [categories[0]]  # close the polygon

    for oem, scores in oems.items():
        scores_closed = scores + [scores[0]]
        fig.add_trace(go.Scatterpolar(
            r=scores_closed,
            theta=cats_closed,
            fill="toself",
            name=oem,
            line=dict(color=colours[oem], width=2),
            fillcolor=colours[oem],
            opacity=0.15,
            hovertemplate=f"<b>{oem}</b><br>%{{theta}}: %{{r}}/10<extra></extra>",
        ))

    fig.update_layout(
        title=dict(
            text="<b>Competitive Moat Scorecard — BMW vs Mercedes vs VW</b><br>"
                 "<sup>Analyst scores 1-10 | BMW leads on brand, financial services, Neue Klasse pipeline</sup>",
            x=0.5, font=dict(size=15)),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=9)),
            angularaxis=dict(tickfont=dict(size=11)),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        plot_bgcolor="white", paper_bgcolor="white",
        height=520, margin=dict(l=80, r=80, t=90, b=80),
    )
    return _save(fig, "04_moat_radar.html")
