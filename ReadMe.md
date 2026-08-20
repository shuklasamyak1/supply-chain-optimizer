# 📦 Global Supply Chain Risk & Operational Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://supply-chain-optimizer-nd2hjpl7rhhkhe7p9nfzme.streamlit.app/)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Status](https://img.shields.io/badge/Deployment-Live-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

An interactive, end-to-end supply chain analytics platform evaluating fulfillment volatility, supplier reliability, and inventory risk across multimodal global logistics networks.

🔗 **Live Interactive Application:** [Launch Dashboard](https://supply-chain-optimizer-nd2hjpl7rhhkhe7p9nfzme.streamlit.app/)

---

## 🖥️ Live Application Demo & Previews

### 🎬 Animated Workflow
![Dashboard Walkthrough](Preview_dashboard.gif)

---

### 📊 Interface Snapshots

**1. Executive KPI Strip & Operational Variance Distributions**
![Dashboard View 1](Dashboard_image.png)

**2. Safety Stock Simulation & Supplier Performance Matrix**
![Dashboard View 2](Dashboard_image2.png)

---

### 🎥 Full Video Walkthrough
Click below to view the high-resolution demonstration recording:

▶️ **[Watch Full Dashboard Walkthrough (MP4)](Recording_using_dashboard.mp4)**

---

## 🎯 Executive Overview & Core Problem

In enterprise logistics, fulfillment volatility directly impacts bottom-line profitability. Unreliable supplier timelines increase inventory holding costs and risk production line shutdowns.

This decision-support tool evaluates **2,500 multimodal shipment records** to:
1. **Track Fulfillment Quality:** Measure On-Time In-Full (OTIF) service rates across supplier tiers.
2. **Quantify Financial Exposure:** Dynamically calculate disruption costs resulting from delivery delays and defective shipments.
3. **Simulate Inventory Buffers:** Model optimal Safety Stock and Reorder Points (ROP) using lead-time and demand variance.

---

## 🚀 Key Features

* **Real-Time Dynamic Filtering:** Slices multi-tier data by suppliers, product categories, and logistics freight modes.
* **Lead-Time Variance Analysis:** Visualizes transit day distributions and outlier spreads via combined Histograms and Box Plots.
* **Supplier Risk & Financial Matrix:** Identifies underperforming partners by plotting OTIF rates against average delay penalties.
* **Inventory Simulation Engine:** Dynamically calculates warehouse buffer requirements:
  $$\text{Safety Stock} = Z \times \sqrt{\bar{L} \cdot \sigma_D^2 + \bar{D}^2 \cdot \sigma_L^2}$$
* **Audit & Export Center:** Instant CSV data extraction for flagged delays and defective shipments.

---

## 🛠️ Tech Stack & Methodologies

* **Analytics & Modeling:** Python, Pandas, NumPy
* **Interactive Visualization:** Plotly Express
* **Application Framework:** Streamlit Community Cloud
* **Mathematical Concepts:** Lognormal/Exponential Distributions, Statistical Variance ($\sigma$), $Z$-Score Service Levels
