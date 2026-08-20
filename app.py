import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Global Supply Chain Risk & Operational Optimizer",
    page_icon="📦",
    layout="wide"
)

# 2. Data Ingestion & Caching
@st.cache_data
def load_data():
    df = pd.read_csv('supply_chain_data.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# 3. Header & Executive Summary
st.title("📦 Enterprise Supply Chain & Operational Risk Suite")
st.markdown("Decision-support analytics: evaluate **On-Time In-Full (OTIF)** performance, quantify **financial disruption costs**, and simulate **buffer inventory** under lead-time variance.")

# 4. Sidebar Controls & Parameters
st.sidebar.header("🕹️ Operational Filters")
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
st.sidebar.header("💶 Disruption Cost Parameters")
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

# 5. Top-Level Executive KPI Strip
total_orders = len(filtered_df)
total_spend = filtered_df['order_value_eur'].sum()
otif_rate = (filtered_df['is_otif'].mean()) * 100 if total_orders > 0 else 0
total_disruption_loss = filtered_df['total_disruption_cost_eur'].sum()
avg_lead_time = filtered_df['actual_lead_time_days'].mean() if total_orders > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Shipments", f"{total_orders:,}")
kpi2.metric("Total Spend", f"€{total_spend:,.0f}")
kpi3.metric("OTIF Success Rate", f"{otif_rate:.1f}%")
kpi4.metric("Disruption Financial Loss", f"€{total_disruption_loss:,.0f}")
kpi5.metric("Avg Lead Time", f"{avg_lead_time:.1f} Days")

st.markdown("---")

# 6. Core Visual Analytics (Charts)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Lead-Time Variance by Freight Mode")
    fig_hist = px.histogram(
        filtered_df, 
        x="actual_lead_time_days", 
        color="shipping_mode", 
        marginal="box",
        title="Actual Lead-Time Spread & Outliers",
        labels={'actual_lead_time_days': 'Actual Lead Time (Days)', 'shipping_mode': 'Freight Mode'},
        template="plotly_dark"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.subheader("🎯 Supplier Reliability & Financial Risk Matrix")
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
        title="OTIF Rate vs Delay Days (Bubble Size = Disruption Loss €)",
        labels={'otif_pct': 'OTIF Rate (%)', 'avg_delay': 'Avg Delay (Days)'},
        template="plotly_dark"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# 7. Safety Stock & Reorder Point Simulation Engine
st.markdown("---")
st.subheader("⚙️ Real-Time Safety Stock & Service Level Engine")
st.markdown("Calculate inventory buffers to mitigate stockout risks based on supplier lead-time volatility ($\sigma_L$) and demand variance ($\sigma_D$).")

sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    daily_demand = st.slider("Average Daily Demand ($\overline{D}$ Units)", min_value=50, max_value=1000, value=250, step=25)
    demand_std = st.slider("Demand Std Deviation ($\sigma_D$)", min_value=5, max_value=200, value=40, step=5)
with sim_col2:
    service_level = st.selectbox("Target Service Level Factor", options=["90% (Z = 1.28)", "95% (Z = 1.65)", "99% (Z = 2.33)"], index=1)
    z_map = {"90% (Z = 1.28)": 1.28, "95% (Z = 1.65)": 1.65, "99% (Z = 2.33)": 2.33}
    z_val = z_map[service_level]

avg_L = filtered_df['actual_lead_time_days'].mean() if total_orders > 0 else 0
std_L = filtered_df['actual_lead_time_days'].std() if total_orders > 0 else 0

# Formula: SS = Z * sqrt(L * σ_D^2 + D^2 * σ_L^2)
ss_units = z_val * np.sqrt((avg_L * (demand_std ** 2)) + ((daily_demand ** 2) * (std_L ** 2))) if total_orders > 0 else 0
reorder_point = (daily_demand * avg_L) + ss_units if total_orders > 0 else 0

r1, r2, r3 = st.columns(3)
r1.metric("Recommended Safety Buffer", f"{int(ss_units):,} Units")
r2.metric("Reorder Point (ROP)", f"{int(reorder_point):,} Units")
r3.metric("Lead-Time Volatility ($\sigma_L$)", f"{std_L:.2f} Days")

# 8. Data Audit & Export Center
st.markdown("---")
st.subheader("📋 Order Audit & Anomaly Export Center")

tab1, tab2 = st.tabs(["Delayed Shipments Log", "Defective Orders Log"])

with tab1:
    delayed_subset = filtered_df[filtered_df['is_delayed']][['order_id', 'order_date', 'supplier', 'shipping_mode', 'promised_lead_time_days', 'actual_lead_time_days', 'delay_days', 'delay_cost_eur']]
    st.dataframe(delayed_subset, use_container_width=True)

with tab2:
    defective_subset = filtered_df[filtered_df['is_defective']][['order_id', 'order_date', 'supplier', 'product_category', 'order_value_eur', 'defect_cost_eur']]
    st.dataframe(defective_subset, use_container_width=True)

# CSV Download Action
csv_export = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Operational Dataset (CSV)",
    data=csv_export,
    file_name="filtered_supply_chain_audit.csv",
    mime="text/csv"
)