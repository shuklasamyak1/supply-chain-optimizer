import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Set default Plotly canvas to clean white
pio.templates.default = "plotly_white"

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

    /* Global Canvas Foundation */
    :root, .stApp {
        --primary-color: #0070AD !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Structured Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 1.5rem !important;
    }
    
    .sidebar-section-title {
        color: #0070AD !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.74rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.9px !important;
        margin-top: 8px !important;
        margin-bottom: 14px !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] label span {
        color: #0F172A !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        margin-bottom: 2px !important;
    }

    /* Clean White Multiselect Shell */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        min-height: 38px !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #0070AD !important;
    }

    /* Refined Multiselect Chips */
    span[data-baseweb="tag"],
    div[data-baseweb="tag"] {
        background-color: #F1F5F9 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 4px !important;
        padding: 1px 6px !important;
        margin: 2px !important;
    }
    span[data-baseweb="tag"] span,
    div[data-baseweb="tag"] span {
        color: #1E293B !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
    }
    span[data-baseweb="tag"] svg,
    div[data-baseweb="tag"] svg {
        fill: #64748B !important;
    }

    /* Slider Styling */
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
        font-size: 0.78rem !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] [data-testid="stTickBarMax"] {
        color: #64748B !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
    }

    /* Executive KPI Cards (No line breaks on numbers) */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .metric-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.35rem;
        font-weight: 700;
        color: #0070AD;
        letter-spacing: -0.5px;
        line-height: 1.2;
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-caption {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #475569;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Native Card Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 18px 20px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
        margin-bottom: 16px !important;
    }

    /* Section & Chart Headers */
    .card-header-title {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.0rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
        margin-bottom: 12px !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #CBD5E1;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border-radius: 6px 6px 0 0 !important;
        color: #64748B !important;
        padding: 8px 16px !important;
        border: 1px solid #E2E8F0 !important;
        border-bottom: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
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

    /* Primary Action Buttons */
    .stButton>button, .stDownloadButton>button {
        background-color: #0070AD !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: 1px solid #005A8C !important;
        border-radius: 6px !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #005A8C !important;
        box-shadow: 0 2px 6px rgba(0, 112, 173, 0.25) !important;
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
st.markdown("<h1 style='margin-bottom: 2px; font-weight: 800; letter-spacing: -0.5px;'>Global Supply Chain Risk & Operational Optimizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #475569; font-size: 0.92rem; margin-top: 0px; margin-bottom: 16px;'>Decision-support analytics: evaluate <b>On-Time In-Full (OTIF)</b> performance, quantify <b>financial disruption write-offs</b>, and simulate <b>buffer inventory</b> under stochastic lead-time variance.</p>", unsafe_allow_html=True)

# 5. Sidebar Controls & Parameters
with st.sidebar:
    st.markdown("<div class='sidebar-section-title'>01 / Operational Filters</div>", unsafe_allow_html=True)
    selected_suppliers = st.multiselect(
        "Suppliers", 
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

    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-title'>02 / Disruption Parameters</div>", unsafe_allow_html=True)
    delay_cost_per_day = st.number_input("Late Delivery Penalty (€/Day)", min_value=50, max_value=5000, value=250, step=50)
    defect_penalty_pct = st.slider("Defect Write-off Ratio (%)", min_value=10, max_value=100, value=50, step=5)

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

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Total Shipments</div><div class='metric-val' style='color: #0F172A;'>{total_orders:,}</div><div class='metric-caption'>Tracked Batches</div></div>""", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Total Spend</div><div class='metric-val'>€{total_spend:,.0f}</div><div class='metric-caption'>Gross Invoiced</div></div>""", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>OTIF Success</div><div class='metric-val' style='color: #059669;'>{otif_rate:.1f}%</div><div class='metric-caption'>Fulfillment Rate</div></div>""", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Disruption Loss</div><div class='metric-val' style='color: #0F172A;'>€{total_disruption_loss:,.0f}</div><div class='metric-caption'>Delays + Penalties</div></div>""", unsafe_allow_html=True)
with kpi5:
    st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Avg Lead Time</div><div class='metric-val' style='color: #0070AD;'>{avg_lead_time:.1f}d</div><div class='metric-caption'>Transit Duration</div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

# 7. Core Visual Analytics (Structured in Distinct Cards)
col_left, col_right = st.columns(2)

with col_left:
    with st.container(border=True):
        st.markdown("<div class='card-header-title'>Lead-Time Variance by Freight Mode</div>", unsafe_allow_html=True)
        fig_hist = px.histogram(
            filtered_df, 
            x="actual_lead_time_days", 
            color="shipping_mode", 
            marginal="box",
            labels={'actual_lead_time_days': 'Actual Lead Time (Days)', 'shipping_mode': 'Freight Mode'},
            color_discrete_sequence=["#0070AD", "#0284C7", "#38BDF8", "#64748B"]
        )
        fig_hist.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", family="Inter, sans-serif"),
            xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0", tickfont=dict(color="#475569")),
            yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0", tickfont=dict(color="#475569")),
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    with st.container(border=True):
        st.markdown("<div class='card-header-title'>Supplier Reliability & Financial Risk Matrix</div>", unsafe_allow_html=True)
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
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", family="Inter, sans-serif"),
            xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0", tickfont=dict(color="#475569")),
            yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0", tickfont=dict(color="#475569")),
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

# 8. Safety Stock & Reorder Point Simulation Engine
with st.container(border=True):
    st.markdown("<div class='card-header-title'>Stochastic Safety Stock & Service Level Buffer Engine</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-top: -6px; margin-bottom: 16px;'>Inventory buffer calculation to safeguard against stockouts under joint demand variance ($\\sigma_D$) and lead-time volatility ($\\sigma_L$).</p>", unsafe_allow_html=True)

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

    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Recommended Buffer</div><div class='metric-val'>{int(ss_units):,} Units</div><div class='metric-caption'>Mitigates stochastic risk</div></div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Reorder Point (ROP)</div><div class='metric-val' style='color: #0F172A;'>{int(reorder_point):,} Units</div><div class='metric-caption'>Purchase order threshold</div></div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""<div class='metric-card'><div class='metric-sub'>Lead-Time Volatility (σ_L)</div><div class='metric-val' style='color: #64748B;'>{std_L:.2f} Days</div><div class='metric-caption'>Empirical node std dev</div></div>""", unsafe_allow_html=True)

# 9. Data Audit & Export Center
with st.container(border=True):
    st.markdown("<div class='card-header-title'>Order Audit & Anomaly Export Center</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Delayed Shipments Log", "Defective Orders Log"])

    with tab1:
        delayed_subset = filtered_df[filtered_df['is_delayed']][['order_id', 'order_date', 'supplier', 'shipping_mode', 'promised_lead_time_days', 'actual_lead_time_days', 'delay_days', 'delay_cost_eur']]
        st.dataframe(delayed_subset, use_container_width=True, hide_index=True)

    with tab2:
        defective_subset = filtered_df[filtered_df['is_defective']][['order_id', 'order_date', 'supplier', 'product_category', 'order_value_eur', 'defect_cost_eur']]
        st.dataframe(defective_subset, use_container_width=True, hide_index=True)

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    csv_export = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Operational Dataset (CSV)",
        data=csv_export,
        file_name="filtered_supply_chain_audit.csv",
        mime="text/csv"
    )
