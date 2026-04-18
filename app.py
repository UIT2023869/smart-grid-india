import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="India Grid — Energy Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f5f0e8;
    color: #1a1a1a;
}

.stApp { background-color: #f5f0e8; }
.main .block-container { padding: 2rem 2.5rem; max-width: 1400px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1a1a1a !important;
    border-right: none;
}
section[data-testid="stSidebar"] * { color: #f5f0e8 !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    letter-spacing: 0.05em;
    padding: 6px 0;
    cursor: pointer;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #888 !important;
    letter-spacing: 0.08em;
}

/* Nav label */
.nav-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #666 !important;
    margin-bottom: 12px;
    display: block;
}

/* Page title */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    line-height: 1.0;
    color: #1a1a1a;
    margin-bottom: 4px;
}
.page-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #888;
    letter-spacing: 0.08em;
    margin-bottom: 32px;
}

/* Divider */
.rule { border: none; border-top: 1px solid #d4cfc7; margin: 24px 0; }

/* KPI cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.kpi-card {
    background: #fff;
    border: 1px solid #e0dbd2;
    border-radius: 4px;
    padding: 20px 22px;
}
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
}
.kpi-sub {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #bbb;
}
.kpi-accent { border-left: 3px solid #c8f04a; }
.kpi-accent2 { border-left: 3px solid #f04a4a; }
.kpi-accent3 { border-left: 3px solid #4ab8f0; }
.kpi-accent4 { border-left: 3px solid #f0a64a; }

/* Section label */
.section-tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 8px;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 20px;
}

/* Insight strip */
.insight {
    background: #1a1a1a;
    color: #f5f0e8;
    border-radius: 4px;
    padding: 16px 20px;
    margin-top: 16px;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    line-height: 1.6;
}
.insight b { color: #c8f04a; }

/* Metrics override */
div[data-testid="stMetric"] {
    background: #fff !important;
    border: 1px solid #e0dbd2 !important;
    border-radius: 4px !important;
    padding: 16px 18px !important;
}
div[data-testid="stMetric"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #999 !important;
}
div[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
}
div[data-testid="stMetricDelta"] { font-size: 11px !important; color: #999 !important; }

/* Tabs */
button[data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #999 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1a1a1a !important;
    border-bottom: 2px solid #1a1a1a !important;
}

/* Logo in sidebar */
.logo-block {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #f5f0e8;
    padding: 8px 0 4px 0;
    letter-spacing: -0.02em;
}
.logo-sub {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #666;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 28px;
}

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Paths ─────────────────────────────────────────────────────
BASE      = os.path.dirname(os.path.abspath(__file__))
EXPORTS   = os.path.join(BASE, 'exports')
PROCESSED = os.path.join(BASE, 'data', 'processed')

# ── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    posoco = pd.read_csv(
        os.path.join(PROCESSED, 'posoco_cleaned.csv'),
        parse_dates=True, index_col='Date'
    )
    forecast_daily   = pd.read_csv(os.path.join(EXPORTS, 'powerbi_forecast_daily.csv'),
                                   parse_dates=True, index_col='Date')
    forecast_monthly = pd.read_csv(os.path.join(EXPORTS, 'powerbi_forecast.csv'),
                                   parse_dates=['Date'])
    yearly  = pd.read_csv(os.path.join(EXPORTS, 'powerbi_yearly.csv'))
    return posoco, forecast_daily, forecast_monthly, yearly

posoco, forecast_daily, forecast_monthly, yearly = load_data()

# ── Chart style helper ────────────────────────────────────────
def style_ax(ax, fig):
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    for spine in ax.spines.values():
        spine.set_color('#e0dbd2')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#999', labelsize=9)
    ax.yaxis.label.set_color('#999')
    ax.xaxis.label.set_color('#999')
    ax.yaxis.label.set_fontsize(10)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-block">⚡ INDIA GRID</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">Energy Intelligence System</div>', unsafe_allow_html=True)

    st.markdown('<span class="nav-label">Navigate</span>', unsafe_allow_html=True)
    page = st.radio("", [
        "Overview",
        "Demand Patterns",
        "Renewables",
        "Forecast",
        "Model"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f'<p>Data: {posoco.index.min().strftime("%b %Y")} — {posoco.index.max().strftime("%b %Y")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p>{len(posoco):,} daily records</p>', unsafe_allow_html=True)
    st.markdown(f'<p>Model: LightGBM · MAPE 1.15%</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown('<div class="page-title">India Energy<br>at a Glance.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">NATIONAL GRID MONITOR · POSOCO DATA · UPDATED MARCH 2026</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    avg  = posoco['India: DemandMet'].mean()
    peak = posoco['India: DemandMet'].max()
    sol  = posoco['India: SolarGen'].sum() if 'India: SolarGen' in posoco.columns else 0
    wind = posoco['India: WindGen'].sum()  if 'India: WindGen'  in posoco.columns else 0

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card kpi-accent">
            <div class="kpi-label">Avg Daily Demand</div>
            <div class="kpi-value">{avg:,.0f}</div>
            <div class="kpi-sub">MU per day</div>
        </div>
        <div class="kpi-card kpi-accent2">
            <div class="kpi-label">All-Time Peak</div>
            <div class="kpi-value">{peak:,.0f}</div>
            <div class="kpi-sub">MU — {posoco['India: DemandMet'].idxmax().strftime('%b %Y')}</div>
        </div>
        <div class="kpi-card kpi-accent3">
            <div class="kpi-label">Total Solar Generated</div>
            <div class="kpi-value">{sol/1e6:.1f}M</div>
            <div class="kpi-sub">MU cumulative</div>
        </div>
        <div class="kpi-card kpi-accent4">
            <div class="kpi-label">Total Wind Generated</div>
            <div class="kpi-value">{wind/1e6:.1f}M</div>
            <div class="kpi-sub">MU cumulative</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-tag">Trend</div><div class="section-title">National Demand — Full History</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(13, 3.5))
    style_ax(ax, fig)
    ax.plot(posoco.index, posoco['India: DemandMet'],
            color='#1a1a1a', linewidth=0.7, alpha=0.85)
    ax.fill_between(posoco.index, posoco['India: DemandMet'],
                    alpha=0.06, color='#1a1a1a')
    ax.set_ylabel('MU')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight">India\'s grid demand has grown <b>steadily year on year</b>, with visible dips during COVID (2020) and a strong recovery afterward. The upward slope reflects industrial growth, rising AC penetration, and EV adoption.</div>', unsafe_allow_html=True)

    if not yearly.empty:
        st.markdown('<hr class="rule">', unsafe_allow_html=True)
        st.markdown('<div class="section-tag">Table</div><div class="section-title">Year-by-Year Breakdown</div>', unsafe_allow_html=True)
        st.dataframe(yearly, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — DEMAND PATTERNS
# ══════════════════════════════════════════════════════════════
elif page == "Demand Patterns":
    st.markdown('<div class="page-title">When India<br>Needs Power.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">SEASONAL · WEEKLY · YEARLY PATTERNS</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Monthly seasonality", "Day of week", "Year on year"])

    with tab1:
        monthly_avg = posoco.groupby(posoco.index.month)['India: DemandMet'].mean()
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        peak_m = monthly_avg.values.argmax()

        fig, ax = plt.subplots(figsize=(12, 4))
        style_ax(ax, fig)
        bar_colors = ['#c8f04a' if i == peak_m else '#e8e3db' for i in range(12)]
        ax.bar(months, monthly_avg.values, color=bar_colors, width=0.6, edgecolor='none')
        ax.set_ylabel('Avg Demand (MU)')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

        st.markdown(f'<div class="insight">Peak demand falls in <b>{months[peak_m]}</b> — driven by summer cooling loads across residential and commercial sectors. Grid planners must ensure reserve capacity of at least 15% above peak.</div>', unsafe_allow_html=True)

    with tab2:
        dow_avg = posoco.groupby(posoco.index.dayofweek)['India: DemandMet'].mean()
        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        weekday_avg = dow_avg[:5].mean()
        weekend_avg = dow_avg[5:].mean()
        diff = ((weekday_avg - weekend_avg) / weekend_avg) * 100

        fig, ax = plt.subplots(figsize=(9, 4))
        style_ax(ax, fig)
        colors = ['#e8e3db','#e8e3db','#e8e3db','#e8e3db','#e8e3db','#f04a4a','#f04a4a']
        ax.bar(days, dow_avg.values, color=colors, width=0.55, edgecolor='none')
        ax.set_ylabel('Avg Demand (MU)')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

        st.markdown(f'<div class="insight">Weekdays run <b>{diff:.1f}% hotter</b> than weekends. The drop on Saturday and Sunday reflects factories and offices going dark — a reliable, exploitable pattern for demand forecasting.</div>', unsafe_allow_html=True)

    with tab3:
        yearly_avg = posoco.groupby(posoco.index.year)['India: DemandMet'].mean()

        fig, ax = plt.subplots(figsize=(12, 4))
        style_ax(ax, fig)
        ax.plot(yearly_avg.index, yearly_avg.values,
                color='#1a1a1a', linewidth=2,
                marker='o', markersize=7,
                markerfacecolor='#c8f04a', markeredgecolor='#1a1a1a', markeredgewidth=1.5)
        for x, y in zip(yearly_avg.index, yearly_avg.values):
            ax.annotate(f'{y:,.0f}', (x, y),
                       textcoords="offset points", xytext=(0, 12),
                       ha='center', color='#666', fontsize=9,
                       fontfamily='monospace')
        ax.set_ylabel('Avg Demand (MU)')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()


# ══════════════════════════════════════════════════════════════
# PAGE 3 — RENEWABLES
# ══════════════════════════════════════════════════════════════
elif page == "Renewables":
    st.markdown('<div class="page-title">The Clean<br>Energy Shift.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">SOLAR · WIND · HYDRO — INDIA\'S GENERATION MIX</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    ren_cols = [c for c in ['India: SolarGen','India: WindGen','India: HydroGen'] if c in posoco.columns]
    labels   = {'India: SolarGen':'Solar','India: WindGen':'Wind','India: HydroGen':'Hydro'}
    clrs     = {'India: SolarGen':'#f0c84a','India: WindGen':'#4af0c8','India: HydroGen':'#4ab8f0'}

    cols = st.columns(len(ren_cols))
    for i, c in enumerate(ren_cols):
        with cols[i]:
            st.metric(labels[c], f"{posoco[c].mean():,.0f} MU/day",
                     f"Peak {posoco[c].max():,.0f}")

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Growth</div><div class="section-title">30-Day Rolling Average by Source</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(13, 4))
    style_ax(ax, fig)
    for c in ren_cols:
        ax.plot(posoco.index, posoco[c].rolling(30).mean(),
                label=labels[c], color=clrs[c], linewidth=1.8)
    ax.set_ylabel('Generation (MU)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.legend(frameon=False, fontsize=10)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight"><b>Solar has gone near-vertical since 2020.</b> India added more solar capacity in 3 years than it did in the previous decade. Wind is steady; hydro stays seasonal — monsoon in, monsoon out.</div>', unsafe_allow_html=True)

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Composition</div><div class="section-title">Share of Renewable Mix</div>', unsafe_allow_html=True)

    totals = {labels[c]: posoco[c].sum() for c in ren_cols}
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor('#ffffff')
    wedge_colors = [clrs[c] for c in ren_cols]
    wedges, texts, autos = ax.pie(
        totals.values(), labels=totals.keys(),
        colors=wedge_colors, autopct='%1.1f%%',
        pctdistance=0.75, startangle=90,
        wedgeprops={'edgecolor':'#fff','linewidth':3},
        textprops={'fontsize': 11, 'color': '#1a1a1a'}
    )
    for a in autos: a.set_fontsize(10); a.set_color('#1a1a1a')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ══════════════════════════════════════════════════════════════
# PAGE 4 — FORECAST
# ══════════════════════════════════════════════════════════════
elif page == "Forecast":
    st.markdown('<div class="page-title">Next 90 Days<br>of Demand.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">AI FORECAST · LIGHTGBM · RECURSIVE PREDICTION</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Avg Forecast", f"{forecast_daily['Forecast_MU'].mean():,.0f} MU", "per day")
    with col2: st.metric("Forecast Peak", f"{forecast_daily['Forecast_MU'].max():,.0f} MU")
    with col3: st.metric("Forecast Low",  f"{forecast_daily['Forecast_MU'].min():,.0f} MU")

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Chart</div><div class="section-title">Historical Context + 90-Day Ahead</div>', unsafe_allow_html=True)

    tail = posoco['India: DemandMet'].iloc[-180:]

    fig, ax = plt.subplots(figsize=(13, 4.5))
    style_ax(ax, fig)

    ax.plot(tail.index, tail.values,
            color='#1a1a1a', linewidth=1.2, label='Historical', alpha=0.8)
    ax.plot(forecast_daily.index, forecast_daily['Forecast_MU'],
            color='#f04a4a', linewidth=2, linestyle='--', label='Forecast')

    lower = forecast_daily['Forecast_MU'] * 0.95
    upper = forecast_daily['Forecast_MU'] * 1.05
    ax.fill_between(forecast_daily.index, lower, upper,
                   alpha=0.12, color='#f04a4a', label='±5% band')
    ax.axvline(tail.index[-1], color='#999', linestyle=':', linewidth=1)

    ax.set_ylabel('Demand (MU)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.legend(frameon=False, fontsize=10)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight">The model picks up the <b>seasonal ramp</b> heading into summer. The ±5% uncertainty band is where grid operators live — they plan capacity for the upper edge, not the midline.</div>', unsafe_allow_html=True)

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Summary</div><div class="section-title">Monthly Forecast Breakdown</div>', unsafe_allow_html=True)

    if 'Month_Name' in forecast_monthly.columns:
        display = forecast_monthly[['Month_Name','Avg_Forecast','Max_Forecast','Min_Forecast']].copy()
        display.columns = ['Month','Avg (MU)','Max (MU)','Min (MU)']
        st.dataframe(display, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — MODEL
# ══════════════════════════════════════════════════════════════
elif page == "Model":
    st.markdown('<div class="page-title">The Model<br>Behind It.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">LIGHTGBM · AUTOML · PYCARET · 1.15% MAPE</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("MAPE",      "1.15%",   "Target < 5%")
    with col2: st.metric("R² Score",  "0.97+",   "Variance explained")
    with col3: st.metric("Algorithm", "LightGBM","AutoML winner")
    with col4: st.metric("Test split","20%",     "Held-out data")

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Validation</div><div class="section-title">Actual vs Predicted on Test Set</div>', unsafe_allow_html=True)

    img_path = os.path.join(EXPORTS, '09_actual_vs_predicted.png')
    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True)

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Competition</div><div class="section-title">All Models Compared</div>', unsafe_allow_html=True)

    model_path = os.path.join(EXPORTS, 'automl_model_comparison.csv')
    if os.path.exists(model_path):
        mdf = pd.read_csv(model_path)
        st.dataframe(mdf, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="insight">
    LightGBM won because it handles <b>lag features and time patterns</b> better than linear models,
    trains faster than XGBoost on this data size, and doesn't overfit on the rolling averages.
    A MAPE of 1.15% means on a 500 MU day, we're off by about 5.75 MU —
    well within operational tolerance for grid planning.
    </div>
    """, unsafe_allow_html=True)
