import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Global Supply Chain Risk & Operational Optimizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Bespoke Theme & Professional Typography Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    /* 1. Global Base Canvas */
    :root, .stApp {
        --primary-color: #0070AD !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* 2. Enterprise Light-Slate Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F1F5F9 !important;
        border-right: 1px solid #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .sidebar-heading {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        font-size: 0.82rem !important;
        letter-spacing: 0.8px !important;
        margin-top: 10px !important;
        margin-bottom: 12px !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] label span {
        color: #0F172A !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }

    /* Sidebar Multiselect Chips */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #E0F2FE !important;
        border: 1px solid #BAE6FD !important;
        border-radius: 4px !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #0369A1 !important;
        font-weight: 600 !important;
    }

    /* Sidebar Sliders & Numeric Inputs */
    section[data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"] {
        background-color: #0070AD !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 0 2px rgba(0, 112, 173, 0.3) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="slider"] > div > div > div {
        background: #0070AD !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="slider"] > div > div {
        background: #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stThumbValue"] {
        background-color: #0070AD !important;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 0.80rem !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] [data-testid="stTickBarMax"] {
        color: #64748B !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.74rem !important;
        font-weight: 600 !important;
    }

    /* 3. Executive Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }
    .metric-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.74rem;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.70rem;
        font-weight: 700;
        color: #0070AD;
        letter-spacing: -0.6px;
        line-height: 1.2;
    }
    .metric-caption {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: #475569;
        font-weight: 500;
        margin-top: 4px;
    }

    /* 4. Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #CBD5E1;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border-radius: 6px 6px 0 0 !important;
        color: #64748B !important;
        padding: 10px 18px !important;
        border: 1px solid #E2E8F0 !important;
        border-bottom: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0070AD !important;
        color: #FFFFFF !important;
        border: 1px solid #0070AD !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }

    /* 5. Typography */
    h1, h2, h3, h4 {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.4px;
    }
    p, span {
        color: #334155;
        font-family: 'Inter', sans-serif;
    }

    /* 6. Primary Action Buttons */
    .stButton>button, .stDownloadButton>button {
        background-color: #0070AD !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        border: 1px solid #005A8C !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #005A8C !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(0, 112, 173, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Data Ingestion & Caching
@st.cache_data
def load_data():
    df = pd.read_csv('supply_chain_data.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# 4. Header & Executive Summary
st.markdown("<h1 style='margin-bottom: 2px;'>Global Supply Chain Risk & Operational Optimizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #475569; font-size: 0.95rem; margin-top: 0px;'>Decision-support analytics: evaluate <b>On-Time In-Full (OTIF)</b> performance, quantify <b>financial disruption write-offs</b>, and simulate <b>buffer inventory</b> under stochastic lead-time variance.</p>", unsafe_allow_html=True)

# 5. Sidebar Controls & Parameters
with st.sidebar:
    st.markdown("<div class='sidebar-heading'>Operational Filters</div>", unsafe_allow_html=True)
    selected_suppliers = st.multiselect(
        "Select Suppliers", 
        options=df['supplier'].unique(), 
        default=df['supplier'].unique()
    )
    selected_modes = st.multiselect(
        "Shipping Modes", 
        options=df['shipping_mode'].unique(), 
        default=df['shipping_mode'].unique()
    )
    selected_categories = st.multiselect(
        "Product Categories", 
        options=df['product_category'].unique(), 
        default=df['product_category'].unique()
    )

    st.markdown("<hr style='border: none; border-top: 1px solid #CBD5E1; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-heading'>Disruption Cost Parameters</div>", unsafe_allow_html=True)
    delay_cost_per_day = st.number_input("Late Delivery Penalty (€/Day)", min_value=50, max_value=5000, value=250, step=50)
    defect_penalty_pct = st.slider("Defect Financial Write-off (%)", min_value=10, max_value=100, value=50, step=5)

# Filter Dataset
filtered_df = df[
    (df['supplier'].isin(selected_suppliers)) & 
    (df['shipping_mode'].isin(selected_modes)) & 
    (df['product_category'].isin(selected_categories))
].copy()

# Add Dynamic Financial Risk Columns
filtered_df['delay_cost_eur'] = filtered_df['delay_days'] * delay_cost_per_day
filtered_df['defect_cost_eur'] = np.where(filtered_df['is_defective'], filtered_df['order_value_eur'] * (defect_penalty_pct / 100), 0)
filtered_df['total_disruption_cost_eur'] = filtered_df['delay_cost_eur'] + filtered_df['defect_cost_eur']

# 6. Top-Level Executive KPI Strip
total_orders = len(filtered_df)
total_spend = filtered_df['order_value_eur'].sum()
otif_rate = (filtered_df['is_otif'].mean()) * 100 if total_orders > 0 else 0
total_disruption_loss = filtered_df['total_disruption_cost_eur'].sum()
avg_lead_time = filtered_df['actual_lead_time_days'].mean() if total_orders > 0 else 0

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Total Shipments</div><div class='metric-val' style='color: #0F172A;'>{total_orders:,}</div><div class='metric-caption'>Tracked Batches</div></div>""", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Total Sourcing Spend</div><div class='metric-val'>€{total_spend:,.0f}</div><div class='metric-caption'>Gross Invoiced</div></div>""", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>OTIF Success Rate</div><div class='metric-val' style='color: #059669;'>{otif_rate:.1f}%</div><div class='metric-caption'>Service Fulfillment</div></div>""", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Disruption Loss</div><div class='metric-val' style='color: #0F172A;'>€{total_disruption_loss:,.0f}</div><div class='metric-caption'>Delays + Write-offs</div></div>""", unsafe_allow_html=True)
with kpi5:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Avg Actual Lead Time</div><div class='metric-val' style='color: #0070AD;'>{avg_lead_time:.1f}d</div><div class='metric-caption'>Transit Duration</div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)

# Plotly Palette Theme Template
PLOTLY_THEME = {
    "layout": {
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor": "#FFFFFF",
        "font": {"color": "#0F172A", "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": "#F1F5F9",
            "zerolinecolor": "#E2E8F0",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11, "color": "#475569"}
        },
        "yaxis": {
            "gridcolor": "#F1F5F9",
            "zerolinecolor": "#E2E8F0",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11, "color": "#475569"}
        }
    }
}

# 7. Core Visual Analytics (Charts)
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<h4 style='color: #0F172A;'>Lead-Time Variance by Freight Mode</h4>", unsafe_allow_html=True)
    fig_hist = px.histogram(
        filtered_df, 
        x="actual_lead_time_days", 
        color="shipping_mode", 
        marginal="box",
        labels={'actual_lead_time_days': 'Actual Lead Time (Days)', 'shipping_mode': 'Freight Mode'},
        color_discrete_sequence=["#0070AD", "#0284C7", "#38BDF8", "#64748B"]
    )
    fig_hist.update_layout(
        template=PLOTLY_THEME,
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.markdown("<h4 style='color: #0F172A;'>Supplier Reliability & Financial Risk Matrix</h4>", unsafe_allow_html=True)
    supplier_agg = filtered_df.groupby('supplier').agg(
        total_orders=('order_id', 'count'),
        otif_pct=('is_otif', lambda x: x.mean() * 100),
        avg_delay=('delay_days', 'mean'),
        disruption_loss=('total_disruption_cost_eur', 'sum')
    ).reset_index()

    fig_bubble = px.scatter(
        supplier_agg, 
        x="otif_pct", 
        y="avg_delay", 
        size="disruption_loss", 
        color="supplier", 
        hover_data=['total_orders', 'disruption_loss'],
        labels={'otif_pct': 'OTIF Rate (%)', 'avg_delay': 'Avg Delay (Days)'},
        color_discrete_sequence=["#0070AD", "#0284C7", "#38BDF8", "#475569", "#0F172A"]
    )
    fig_bubble.update_layout(
        template=PLOTLY_THEME,
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# 8. Safety Stock & Reorder Point Simulation Engine
st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #0F172A;'>Stochastic Safety Stock & Service Level Buffer Engine</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 0.88rem;'>Calculate mathematically rigorous inventory buffers to protect against stockout risk under supplier lead-time volatility ($\\sigma_L$) and demand variance ($\\sigma_D$).</p>", unsafe_allow_html=True)

sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    daily_demand = st.slider("Average Daily Demand (D̄ Units)", min_value=50, max_value=1000, value=250, step=25)
    demand_std = st.slider("Daily Demand Std Deviation (σ_D)", min_value=5, max_value=200, value=40, step=5)
with sim_col2:
    service_level = st.selectbox("Target Service Level Factor (Z)", options=["90% (Z = 1.28)", "95% (Z = 1.65)", "99% (Z = 2.33)"], index=1)
    z_map = {"90% (Z = 1.28)": 1.28, "95% (Z = 1.65)": 1.65, "99% (Z = 2.33)": 2.33}
    z_val = z_map[service_level]

avg_L = filtered_df['actual_lead_time_days'].mean() if total_orders > 0 else 0
std_L = filtered_df['actual_lead_time_days'].std() if total_orders > 0 else 0

# Formula: SS = Z * sqrt(L * σ_D^2 + D^2 * σ_L^2)
ss_units = z_val * np.sqrt((avg_L * (demand_std ** 2)) + ((daily_demand ** 2) * (std_L ** 2))) if total_orders > 0 else 0
reorder_point = (daily_demand * avg_L) + ss_units if total_orders > 0 else 0

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Recommended Safety Buffer</div><div class='metric-val'>{int(ss_units):,} Units</div><div class='metric-caption'>Mitigates dual variability</div></div>""", unsafe_allow_html=True)
with r2:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Reorder Point (ROP)</div><div class='metric-val' style='color: #0F172A;'>{int(reorder_point):,} Units</div><div class='metric-caption'>Trigger purchase order threshold</div></div>""", unsafe_allow_html=True)
with r3:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Lead-Time Volatility (σ_L)</div><div class='metric-val' style='color: #64748B;'>{std_L:.2f} Days</div><div class='metric-caption'>Empirical node standard deviation</div></div>""", unsafe_allow_html=True)

# 9. Data Audit & Export Center
st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 28px 0;'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #0F172A;'>Order Audit & Anomaly Export Center</h3>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Delayed Shipments Log", "Defective Orders Log"])

with tab1:
    delayed_subset = filtered_df[filtered_df['is_delayed']][['order_id', 'order_date', 'supplier', 'shipping_mode', 'promised_lead_time_days', 'actual_lead_time_days', 'delay_days', 'delay_cost_eur']]
    st.dataframe(delayed_subset, use_container_width=True, hide_index=True)

with tab2:
    defective_subset = filtered_df[filtered_df['is_defective']][['order_id', 'order_date', 'supplier', 'product_category', 'order_value_eur', 'defect_cost_eur']]
    st.dataframe(defective_subset, use_container_width=True, hide_index=True)

# CSV Download Action
csv_export = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Filtered Operational Dataset (CSV)",
    data=csv_export,
    file_name="filtered_supply_chain_audit.csv",
    mime="text/csv"
)
