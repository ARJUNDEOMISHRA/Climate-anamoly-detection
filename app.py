
# ============================================================
# app.py — Actionable Climate Intelligence Dashboard
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os, io

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_collection import collect_city_data, INDIAN_CITIES
from anomaly import detect_anomalies
from forecast import forecast_temperature
from recommendations import (
    get_recommendations, get_dominant_anomaly,
    get_summary_stats, PRIORITY_CONFIG, SECTOR_ICONS
)
from risk_score import calculate_risk_score, RISK_COLORS, RISK_ICONS

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Climate Intelligence AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0a0e1a; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 24px;
    border: 1px solid rgba(0,198,255,0.2);
}
.hero-title {
    font-size: 2.6rem; font-weight: 800;
    background: linear-gradient(90deg, #00C6FF, #0072FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 4px 0;
}
.hero-sub { color: #8ba4c0; font-size: 1.05rem; margin: 0; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1a1f35, #12172a);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 24px;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #00C6FF, #0072FF);
    border-radius: 4px 0 0 4px;
}
.metric-label { color: #8ba4c0; font-size: 0.8rem; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; }
.metric-value { color: #ffffff; font-size: 2rem; font-weight: 800; line-height: 1; }
.metric-delta { font-size: 0.8rem; margin-top: 4px; }

/* Section headers */
.section-header {
    font-size: 1.35rem; font-weight: 700; color: #e2e8f0;
    border-bottom: 2px solid rgba(0,198,255,0.3);
    padding-bottom: 8px; margin: 28px 0 16px 0;
}

/* Action Center cards */
.sector-card {
    background: linear-gradient(135deg, #141928, #0f1520);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.06);
    transition: transform 0.2s;
}
.sector-card:hover { transform: translateY(-2px); }
.sector-title { font-size: 1.1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 8px; }
.priority-badge {
    display: inline-block;
    padding: 2px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase;
    margin-bottom: 12px;
}
.action-item {
    color: #b0bec5; font-size: 0.88rem;
    padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
    line-height: 1.5;
}
.action-item:last-child { border-bottom: none; }

/* Anomaly type pill */
.anom-pill {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 700; letter-spacing: 0.04em;
}

/* Risk alert box */
.risk-alert {
    border-radius: 12px; padding: 18px 24px; margin: 16px 0;
    border-left: 5px solid;
}

/* Data source badge */
.source-badge {
    display: inline-block; background: rgba(0,198,255,0.1);
    border: 1px solid rgba(0,198,255,0.3);
    color: #00C6FF; border-radius: 20px;
    padding: 3px 12px; font-size: 0.78rem; font-weight: 600;
}

/* Tab styling override */
.stTabs [role="tablist"] { background: #111827; border-radius: 10px; padding: 4px; }
.stTabs [role="tab"]     { color: #6b7280 !important; font-weight: 600; border-radius: 8px; }
.stTabs [aria-selected="true"] { background: #1d4ed8 !important; color: #fff !important; }

/* Hide Streamlit default header */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Climate Intelligence AI")
    st.markdown("---")
    st.markdown("### 🏙️ Select City")
    city_key = st.selectbox(
        "Indian City", list(INDIAN_CITIES.keys()), index=0,
        label_visibility="collapsed"
    )
    st.markdown(f"**State:** {INDIAN_CITIES[city_key]['state']}")
    st.markdown(f"**Lat / Lon:** `{INDIAN_CITIES[city_key]['lat']}` / `{INDIAN_CITIES[city_key]['lon']}`")
    st.markdown("---")
    with st.spinner("Fetching climate data…"):
        df_raw = collect_city_data(city_key)

    df_raw["date"] = pd.to_datetime(df_raw["date"])
    df = detect_anomalies(df_raw)

    source = df["data_source"].iloc[0] if "data_source" in df.columns else "Unknown"
    st.markdown(f"<div class='source-badge'>{source}</div>", unsafe_allow_html=True)
    st.markdown(f"**Records:** {len(df):,}")

    stats           = get_summary_stats(df)
    risk_score, risk_level = calculate_risk_score(df)
    dominant_type   = get_dominant_anomaly(df)
    recs            = get_recommendations(dominant_type)

    st.markdown("---")
    st.markdown(f"### {RISK_ICONS[risk_level]} Risk Level")
    st.markdown(
        f"<div style='font-size:2.2rem;font-weight:800;color:{RISK_COLORS[risk_level]}'>"
        f"{risk_level}</div>", unsafe_allow_html=True
    )
    st.metric("Risk Score", f"{risk_score}/100")
    st.metric("Anomalies Detected", stats["n_anomalies"])
    st.metric("Anomaly Rate", f"{stats['anomaly_rate']}%")

# ────────────────────────────────────────────────────────────
# HERO BANNER
# ────────────────────────────────────────────────────────────
city_name_clean = city_key.split(" ", 1)[-1]
st.markdown(f"""
<div class='hero-banner'>
  <p class='hero-title'>🌍 Actionable Climate Intelligence</p>
  <p class='hero-sub'>
    AI-powered anomaly detection · Real-time forecasting · Sector-specific response plans
    &nbsp;&nbsp;|&nbsp;&nbsp; <strong>📍 {city_name_clean}</strong>
  </p>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
# TABS
# ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Overview",
    "🔍 Anomaly Explorer",
    "🎯 Action Center",
    "🔮 Forecast",
])

# ═══════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════
with tab1:
    # Top metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Risk Score</div>
            <div class='metric-value' style='color:{RISK_COLORS[risk_level]}'>{risk_score}</div>
            <div class='metric-delta' style='color:{RISK_COLORS[risk_level]}'>{RISK_ICONS[risk_level]} {risk_level}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Total Records</div>
            <div class='metric-value'>{stats['total_records']:,}</div>
            <div class='metric-delta' style='color:#8ba4c0'>365-day dataset</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Anomalies Found</div>
            <div class='metric-value' style='color:#FF4B4B'>{stats['n_anomalies']}</div>
            <div class='metric-delta' style='color:#FF4B4B'>{stats['anomaly_rate']}% of data</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Max Severity</div>
            <div class='metric-value' style='color:#FF9000'>{stats['max_severity']}</div>
            <div class='metric-delta' style='color:#8ba4c0'>Avg: {stats['avg_severity']}/100</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Risk Gauge + Dominant anomaly
    col_g, col_info = st.columns([1, 1])
    with col_g:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Composite Risk Score", "font": {"size": 16, "color": "#8ba4c0"}},
            number={"font": {"size": 52, "color": RISK_COLORS[risk_level]}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#4a5568"},
                "bar":  {"color": RISK_COLORS[risk_level], "thickness": 0.25},
                "bgcolor": "#1a1f35",
                "steps": [
                    {"range": [0, 25],  "color": "rgba(0,200,81,0.15)"},
                    {"range": [25, 50], "color": "rgba(255,215,0,0.15)"},
                    {"range": [50, 75], "color": "rgba(255,144,0,0.15)"},
                    {"range": [75, 100],"color": "rgba(255,75,75,0.15)"},
                ],
                "threshold": {"line": {"color": "white", "width": 2},
                              "thickness": 0.8, "value": risk_score},
            },
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white", "family": "Inter"},
            height=280, margin=dict(t=40, b=10, l=20, r=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_info:
        st.markdown("<div class='section-header'>🚨 Active Climate Alert</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='risk-alert' style='background:rgba(255,75,75,0.08);border-color:{recs["color"]}'>
            <div style='font-size:2.4rem'>{recs["icon"]}</div>
            <div style='font-size:1.3rem;font-weight:800;color:{recs["color"]};margin:6px 0'>{recs["label"]}</div>
            <div style='color:#b0bec5;font-size:0.9rem'>{recs["description"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Type breakdown
        if stats["type_counts"]:
            type_df = pd.DataFrame(
                list(stats["type_counts"].items()), columns=["Type", "Count"]
            ).sort_values("Count", ascending=False)
            st.dataframe(type_df, use_container_width=True, hide_index=True)

    # Temperature timeline
    st.markdown("<div class='section-header'>📈 Temperature Timeline with Anomalies</div>",
                unsafe_allow_html=True)
    df_plot = df.copy()
    df_plot["label"] = df_plot["anomaly_type"].apply(
        lambda x: "Normal" if x == "NORMAL" else x
    )
    fig_timeline = go.Figure()
    # Normal line
    normal_df = df_plot[df_plot["anomaly"] == 1]
    fig_timeline.add_trace(go.Scatter(
        x=normal_df["date"], y=normal_df["temperature"],
        mode="lines", name="Normal",
        line=dict(color="#4a90d9", width=1.5),
    ))
    # Anomaly markers by type
    type_colors = {"HEAT_WAVE":"#FF4B4B","COLD_SNAP":"#00B4FF",
                   "EXTREME_RAIN":"#845EC2","DROUGHT":"#FF9000","COMPOUND":"#FF6B6B"}
    for atype, acolor in type_colors.items():
        sub = df_plot[(df_plot["anomaly"] == -1) & (df_plot["anomaly_type"] == atype)]
        if len(sub) > 0:
            fig_timeline.add_trace(go.Scatter(
                x=sub["date"], y=sub["temperature"],
                mode="markers", name=atype,
                marker=dict(color=acolor, size=8, symbol="circle",
                            line=dict(width=1, color="white")),
                hovertemplate=f"<b>{atype}</b><br>Date: %{{x}}<br>Temp: %{{y:.1f}}°C<br>Severity: %{{customdata}}",
                customdata=sub["severity"],
            ))
    fig_timeline.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,21,32,0.9)",
        font=dict(color="white", family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Date"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Temperature (°C)"),
        legend=dict(bgcolor="rgba(0,0,0,0.4)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
        height=360, margin=dict(t=20, b=20, l=10, r=10),
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    # City map
    st.markdown("<div class='section-header'>🗺️ City Location & Anomaly Hotspot</div>",
                unsafe_allow_html=True)
    anom_only = df[df["anomaly"] == -1].copy()
    if len(anom_only) > 0:
        fig_map = px.scatter_mapbox(
            anom_only, lat="lat", lon="lon",
            color="anomaly_type", size="severity", size_max=30,
            color_discrete_map=type_colors,
            hover_data={"date": True, "temperature": ":.1f",
                        "severity": True, "lat": False, "lon": False},
            mapbox_style="open-street-map",
            zoom=6, center={"lat": anom_only["lat"].mean(), "lon": anom_only["lon"].mean()},
            title="",
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            height=380, margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(bgcolor="rgba(0,0,0,0.6)"),
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No anomalies recorded — city is in a stable climate period. 🟢")


# ═══════════════════════════════════════════════════════════
# TAB 2 — ANOMALY EXPLORER
# ═══════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>🔬 Anomaly Type Distribution</div>",
                unsafe_allow_html=True)
    anom_df = df[df["anomaly"] == -1].copy()
    col_a, col_b = st.columns(2)
    with col_a:
        if len(anom_df) > 0:
            type_counts = anom_df["anomaly_type"].value_counts().reset_index()
            type_counts.columns = ["Anomaly Type", "Count"]
            fig_bar = px.bar(
                type_counts, x="Anomaly Type", y="Count",
                color="Anomaly Type",
                color_discrete_map={k: v for k, v in type_colors.items()},
                template="plotly_dark",
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,21,32,0.9)",
                showlegend=False, height=320, margin=dict(t=10, b=10, l=10, r=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        if len(anom_df) > 0:
            fig_scat = px.scatter(
                df, x="temperature", y="precipitation",
                color=df["anomaly"].map({1: "Normal", -1: "Anomaly"}),
                color_discrete_map={"Normal": "#4a90d9", "Anomaly": "#FF4B4B"},
                size="severity", size_max=18,
                hover_data=["date", "anomaly_type"],
                template="plotly_dark",
                labels={"temperature": "Temperature (°C)", "precipitation": "Precipitation (mm)"},
            )
            fig_scat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,21,32,0.9)",
                height=320, margin=dict(t=10, b=10, l=10, r=10),
                legend_title="",
            )
            st.plotly_chart(fig_scat, use_container_width=True)

    st.markdown("<div class='section-header'>📋 Top Anomaly Events</div>", unsafe_allow_html=True)
    if len(anom_df) > 0:
        display = (
            anom_df[["date", "anomaly_type", "severity", "temperature", "precipitation",
                      "z_temp", "z_precip"]]
            .sort_values("severity", ascending=False)
            .head(20)
            .reset_index(drop=True)
        )
        display.columns = ["Date", "Type", "Severity", "Temp (°C)", "Precip (mm)",
                           "Z-Temp", "Z-Precip"]
        display["Date"] = display["Date"].dt.strftime("%Y-%m-%d")
        display["Temp (°C)"] = display["Temp (°C)"].round(1)
        display["Precip (mm)"] = display["Precip (mm)"].round(2)
        display["Z-Temp"]   = display["Z-Temp"].round(2)
        display["Z-Precip"] = display["Z-Precip"].round(2)
        st.dataframe(display, use_container_width=True, hide_index=True)

        # CSV download
        csv = display.to_csv(index=False)
        st.download_button(
            "⬇️ Download Anomaly Report (CSV)", csv,
            file_name=f"climate_anomalies_{city_name_clean.replace(' ','_')}.csv",
            mime="text/csv",
        )
    else:
        st.success("✅ No anomalies detected in this dataset.")


# ═══════════════════════════════════════════════════════════
# TAB 3 — ACTION CENTER  🎯
# ═══════════════════════════════════════════════════════════
with tab3:
    # Alert header
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(255,75,75,0.12),rgba(255,144,0,0.06));
                border:1px solid {recs["color"]}33; border-radius:16px; padding:24px 32px; margin-bottom:24px;'>
      <div style='font-size:3rem; line-height:1'>{recs["icon"]}</div>
      <div style='font-size:1.8rem;font-weight:800;color:{recs["color"]};margin:10px 0 4px'>
        {recs["label"]}
      </div>
      <div style='color:#b0bec5;font-size:0.95rem'>{recs["description"]}</div>
      <div style='margin-top:12px'>
        <span class='anom-pill' style='background:{recs["color"]}22;color:{recs["color"]};
              border:1px solid {recs["color"]}55'>
          📍 {city_name_clean} &nbsp;|&nbsp; Risk Score: {risk_score}/100 &nbsp;|&nbsp;
          {stats["n_anomalies"]} anomaly events detected
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>🎯 Sector-Specific Action Plans</div>",
                unsafe_allow_html=True)
    st.markdown(
        "*The following response plans are generated based on the dominant anomaly pattern "
        "detected by our AI engine. Prioritize **CRITICAL** actions first.*"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Sort sectors by priority
    sectors_ordered = sorted(
        ["Agriculture", "Health", "Infrastructure", "Water"],
        key=lambda s: PRIORITY_CONFIG[recs[s]["priority"]]["order"]
    )

    col_left, col_right = st.columns(2)
    for i, sector in enumerate(sectors_ordered):
        sector_data = recs[sector]
        priority    = sector_data["priority"]
        p_cfg       = PRIORITY_CONFIG[priority]
        icon        = SECTOR_ICONS[sector]
        col         = col_left if i % 2 == 0 else col_right

        with col:
            actions_html = "".join(
                f"<div class='action-item'>{a}</div>" for a in sector_data["actions"]
            )
            st.markdown(f"""
            <div class='sector-card'>
              <div class='sector-title'>{icon} {sector}</div>
              <span class='priority-badge'
                    style='background:{p_cfg["color"]}22;color:{p_cfg["color"]};
                           border:1px solid {p_cfg["color"]}55'>
                {p_cfg["icon"]} {priority} PRIORITY
              </span>
              {actions_html}
            </div>
            """, unsafe_allow_html=True)

    # Summary alert report download
    st.markdown("---")
    st.markdown("### 📄 Download Action Report")
    report_lines = [
        f"CLIMATE INTELLIGENCE ALERT REPORT",
        f"City: {city_name_clean}",
        f"Data Source: {source}",
        f"Risk Level: {risk_level} ({risk_score}/100)",
        f"Active Alert: {recs['label']}",
        f"Total Anomalies: {stats['n_anomalies']} ({stats['anomaly_rate']}%)",
        f"Max Severity: {stats['max_severity']}/100",
        "",
    ]
    for sector in sectors_ordered:
        sector_data = recs[sector]
        report_lines.append(f"=== {SECTOR_ICONS[sector]} {sector.upper()} [{sector_data['priority']} PRIORITY] ===")
        for act in sector_data["actions"]:
            clean_act = act.replace("📌","").replace("🌾","").replace("⏰","").replace("🐄","") \
                          .replace("🌱","").replace("🚨","").replace("🏢","").replace("🚑","") \
                          .replace("💧","").replace("📵","").replace("⚡","").replace("🛣️","") \
                          .replace("🔧","").replace("🚆","").replace("📊","").replace("🚫","") \
                          .replace("🌊","").strip()
            report_lines.append(f"  • {clean_act}")
        report_lines.append("")
    report_text = "\n".join(report_lines)
    st.download_button(
        "⬇️ Download Full Action Report (TXT)", report_text,
        file_name=f"climate_action_report_{city_name_clean.replace(' ','_')}.txt",
        mime="text/plain",
    )

# ═══════════════════════════════════════════════════════════
# TAB 4 — FORECAST
# ═══════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>🔮 14-Day Temperature Forecast</div>",
                unsafe_allow_html=True)

    FORECAST_DAYS = 14
    preds, lower, upper = forecast_temperature(df, days=FORECAST_DAYS)

    if len(preds) > 0:
        last_date    = df["date"].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=FORECAST_DAYS)

        fig_fc = go.Figure()
        # Historical (last 60 days)
        hist = df.sort_values("date").tail(60)
        fig_fc.add_trace(go.Scatter(
            x=hist["date"], y=hist["temperature"],
            mode="lines", name="Historical",
            line=dict(color="#4a90d9", width=2),
        ))
        # Confidence band
        fig_fc.add_trace(go.Scatter(
            x=list(future_dates) + list(future_dates[::-1]),
            y=list(upper) + list(lower[::-1]),
            fill="toself",
            fillcolor="rgba(255,144,0,0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name="95% Confidence Band",
            showlegend=True,
        ))
        # Forecast line
        fig_fc.add_trace(go.Scatter(
            x=future_dates, y=preds,
            mode="lines+markers", name="Forecast",
            line=dict(color="#FF9000", width=2.5, dash="dot"),
            marker=dict(size=7, color="#FF9000"),
        ))
        # Threshold annotation
        if max(preds) > 40:
            fig_fc.add_hline(y=40, line_dash="dash", line_color="#FF4B4B",
                             annotation_text="⚠️ Heat Wave Threshold (40°C)")

        fig_fc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,21,32,0.9)",
            font=dict(color="white", family="Inter"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Date"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Temperature (°C)"),
            legend=dict(bgcolor="rgba(0,0,0,0.4)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
            height=420, margin=dict(t=20, b=20, l=10, r=10),
        )
        st.plotly_chart(fig_fc, use_container_width=True)

        # Forecast table
        fc_df = pd.DataFrame({
            "Date": future_dates.strftime("%Y-%m-%d"),
            "Forecast Temp (°C)": preds.round(2),
            "Lower Bound (°C)":   lower.round(2),
            "Upper Bound (°C)":   upper.round(2),
        })
        st.dataframe(fc_df, use_container_width=True, hide_index=True)

        # Forecast risk note
        avg_fc = np.mean(preds)
        cur_avg = df["temperature"].tail(30).mean()
        delta   = avg_fc - cur_avg
        if delta > 2:
            st.warning(f"⚠️ Forecast shows temperatures rising **+{delta:.1f}°C** above recent average. Risk of heat stress increasing.")
        elif delta < -2:
            st.info(f"❄️ Forecast shows temperatures dropping **{delta:.1f}°C** below recent average. Cold snap risk.")
        else:
            st.success(f"✅ Forecast temperatures are within normal range (Δ{delta:+.1f}°C vs last 30 days).")

        # Download forecast
        csv_fc = fc_df.to_csv(index=False)
        st.download_button(
            "⬇️ Download Forecast (CSV)", csv_fc,
            file_name=f"forecast_{city_name_clean.replace(' ','_')}.csv",
            mime="text/csv",
        )
    else:
        st.error("Insufficient data for forecasting.")