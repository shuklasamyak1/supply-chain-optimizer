import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Global Supply Chain Risk & Operational Optimizer",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Bespoke Theme & Professional Typography Styling
# Palette:
# #04429C (Deep Midnight Blue)
# #0BC8BD (Dark Turquoise / Vibrant Cyan)
# #FFE66D (Warm Gold / Khaki)
# #FEA6A2 (Light Coral / Salmon)
st.markdown("""
<style>
    /* Professional Typography Ingestion */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    /* Global Base */
    .stApp {
        background-color: #032b69;
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #04429C !important;
        border-right: 1px solid rgba(11, 200, 189, 0.25) !important;
        font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Executive Glass Metric Containers */
    .metric-card {
        background: #063980;
        border: 1px solid rgba(11, 200, 189, 0.3);
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .metric-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #FFE66D;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 3px;
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 700;
        color: #0BC8BD;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .metric-caption {
        font-family: 'Inter', sans-serif;
        font-size: 0.74rem;
        color: #E2E8F0;
        margin-top: 3px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(11, 200, 189, 0.25);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #04429C !important;
        border-radius: 6px 6px 0 0 !important;
        color: #E2E8F0 !important;
        padding: 8px 16px !important;
        border: 1px solid rgba(11, 200, 189, 0.2) !important;
        border-bottom: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #063980 !important;
        color: #FFE66D !important;
        border: 1px solid #0BC8BD !important;
        border-bottom: 2px solid #0BC8BD !important;
        font-weight: 700 !important;
    }

    /* Headings & Text */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.4px;
    }
    p, span, label {
        color: #F1F5F9;
        font-family: 'Inter', sans-serif;
    }

    /* Primary Action Buttons */
    .stButton>button, .stDownloadButton>button {
        background-color: #0BC8BD !important;
        color: #04429C !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #FFE66D !important;
        color: #04429C !important;
        box-shadow: 0 0 12px rgba(11, 200, 189, 0.4) !important;
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
st.markdown("<h1 style='margin-bottom: 2px;'>📦 Global Supply Chain Risk & Operational Optimizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #0BC8BD; font-size: 0.95rem; margin-top: 0px;'>Decision-support analytics: evaluate <b>On-Time In-Full (OTIF)</b> performance, quantify <b>financial disruption write-offs</b>, and simulate <b>buffer inventory</b> under stochastic lead-time variance.</p>", unsafe_allow_html=True)

# 5. Sidebar Controls & Parameters
st.sidebar.markdown("<h3 style='color: #FFE66D;'>🕹️ Operational Filters</h3>", unsafe_allow_html=True)
selected_suppliers = st.sidebar.multiselect(
    "Select Suppliers", 
    options=df['supplier'].unique(), 
    default=df['supplier'].unique()
)
selected_modes = st.sidebar.multiselect(
    "Shipping Modes", 
    options=df['shipping_mode'].unique(), 
    default=df['shipping_mode'].unique()
)
selected_categories = st.sidebar.multiselect(
    "Product Categories", 
    options=df['product_category'].unique(), 
    default=df['product_category'].unique()
)

# Sidebar Financial Parameter
st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #FFE66D;'>💶 Disruption Cost Parameters</h3>", unsafe_allow_html=True)
delay_cost_per_day = st.sidebar.number_input("Late Delivery Penalty (€/Day)", min_value=50, max_value=5000, value=250, step=50)
defect_penalty_pct = st.sidebar.slider("Defect Financial Write-off (%)", min_value=10, max_value=100, value=50, step=5)

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

st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Total Shipments</div><div class='metric-val'>{total_orders:,}</div><div class='metric-caption'>Tracked Batches</div></div>""", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Total Sourcing Spend</div><div class='metric-val'>€{total_spend:,.0f}</div><div class='metric-caption'>Gross Invoiced</div></div>""", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>OTIF Success Rate</div><div class='metric-val' style='color: #FFE66D;'>{otif_rate:.1f}%</div><div class='metric-caption'>Service Fulfillment</div></div>""", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Disruption Loss</div><div class='metric-val' style='color: #FEA6A2;'>€{total_disruption_loss:,.0f}</div><div class='metric-caption'>Delays + Write-offs</div></div>""", unsafe_allow_html=True)
with kpi5:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Avg Actual Lead Time</div><div class='metric-val'>{avg_lead_time:.1f}d</div><div class='metric-caption'>Transit Duration</div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# Plotly Palette Theme Template
PLOTLY_THEME = {
    "layout": {
        "paper_bgcolor": "#063980",
        "plot_bgcolor": "#042c67",
        "font": {"color": "#FFFFFF", "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": "rgba(11, 200, 189, 0.15)",
            "zerolinecolor": "rgba(11, 200, 189, 0.2)",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11}
        },
        "yaxis": {
            "gridcolor": "rgba(11, 200, 189, 0.15)",
            "zerolinecolor": "rgba(11, 200, 189, 0.2)",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11}
        }
    }
}

# 7. Core Visual Analytics (Charts)
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📊 Lead-Time Variance by Freight Mode")
    fig_hist = px.histogram(
        filtered_df, 
        x="actual_lead_time_days", 
        color="shipping_mode", 
        marginal="box",
        labels={'actual_lead_time_days': 'Actual Lead Time (Days)', 'shipping_mode': 'Freight Mode'},
        color_discrete_sequence=["#0BC8BD", "#FFE66D", "#FEA6A2", "#60A5FA"]
    )
    fig_hist.update_layout(
        template=PLOTLY_THEME,
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.markdown("### 🎯 Supplier Reliability & Financial Risk Matrix")
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
        color_discrete_sequence=["#0BC8BD", "#FFE66D", "#FEA6A2", "#93C5FD", "#34D399"]
    )
    fig_bubble.update_layout(
        template=PLOTLY_THEME,
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# 8. Safety Stock & Reorder Point Simulation Engine
st.markdown("---")
st.markdown("### ⚙️ Stochastic Safety Stock & Service Level Buffer Engine")
st.markdown("<p style='color: #0BC8BD; font-size: 0.88rem;'>Calculate mathematically rigorous inventory buffers to protect against stockout risk under supplier lead-time volatility ($\\sigma_L$) and demand variance ($\\sigma_D$).</p>", unsafe_allow_html=True)

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
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Reorder Point (ROP)</div><div class='metric-val' style='color: #FFE66D;'>{int(reorder_point):,} Units</div><div class='metric-caption'>Trigger purchase order threshold</div></div>""", unsafe_allow_html=True)
with r3:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Lead-Time Volatility (σ_L)</div><div class='metric-val' style='color: #FEA6A2;'>{std_L:.2f} Days</div><div class='metric-caption'>Empirical node standard deviation</div></div>""", unsafe_allow_html=True)

# 9. Data Audit & Export Center
st.markdown("---")
st.markdown("### 📋 Order Audit & Anomaly Export Center")

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
    label="📥 Download Filtered Operational Dataset (CSV)",
    data=csv_export,
    file_name="filtered_supply_chain_audit.csv",
    mime="text/csv"
)
