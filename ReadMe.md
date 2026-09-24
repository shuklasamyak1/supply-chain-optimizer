# 📦 Global Supply Chain Risk & Operational Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://supply-chain-optimizer-nd2hjpl7rhhkhe7p9nfzme.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

An enterprise-grade operational risk analytics suite that evaluates **On-Time In-Full (OTIF)** fulfillment, quantifies **empirical financial disruption losses**, and simulates **stochastic buffer inventory** (Safety Stock & Reorder Points) under compound lead-time ($\sigma_L$) and demand ($\sigma_D$) volatility.

---

## 🎬 Live Platform Walkthrough

### Executive Terminal & Risk Engine Demo
https://github.com/user-attachments/assets/Dashboard_Preview.mp4

> **Interactive Cockpit:** Real-time multi-echelon filtering across suppliers, freight modes, and SKUs to quantify financial delay write-offs and optimize working capital allocation.

---

## 📸 Platform Previews

### 1. Executive Cockpit & KPI Strip
![Main Cockpit](Main_Page.png)

### 2. Lead-Time Variance & Multi-Modal Spread
![Lead Time Spread](Preview1.png)

### 3. Supplier OTIF vs. Disruption Loss Matrix
![Supplier Risk Matrix](Preview2.png)

### 4. Stochastic Safety Stock & Service Level Buffer Engine
![Inventory Simulation](Preview3.png)

---

## 📌 Executive Architecture & Problem Framing

Global procurement networks frequently suffer margin leakage caused by unmonitored supplier delay variance, defect write-offs, and stockouts. Traditional ERP dashboards report static historical averages without linking delivery variance to working capital risk.

This engine bridges descriptive logistics metrics with prescriptive financial controls by integrating:
1. **Dynamic Disruption Accounting:** Real-time calculation of empirical late delivery penalties and defect write-offs tied directly to invoice values.
2. **Multi-Modal Transit Variance:** Empirical distribution modeling across Air, Ocean, Rail, and Road freight modes to detect fat-tail transit risks.
3. **Compound Variability Buffer Simulation:** Formulates safety stock ($SS$) and continuous-review reorder point ($ROP$) policies accounting for simultaneous demand swings and supplier transit volatility.
4. **Audit & Anomaly Isolation:** Granular exception logging and automated CSV extraction of non-compliant shipment batches.

---

## 🧮 Mathematical & Econometric Formulations

### 1. Dynamic Financial Disruption Loss Function
Disruption impact is computed across historical shipments without imposing restrictive distribution assumptions:

$$\text{Loss}_{\text{Total}} = \sum_{k=1}^{M} \left[ \Delta t_k \cdot C_{\text{delay}} + \mathbb{I}_{(\text{defective}_k)} \cdot V_k \cdot \rho_{\text{write-off}} \right]$$

Where:
* $M$: Total shipment count across selected lanes.
* $\Delta t_k = \max(0, t_{\text{actual}, k} - t_{\text{promised}, k})$: Delay duration in days.
* $C_{\text{delay}}$: Negotiated contractual penalty rate per day (€/day).
* $\mathbb{I}_{(\text{defective}_k)} \in \{0, 1\}$: Binary indicator variable for defective delivery batches.
* $V_k$: Gross invoice value of shipment $k$.
* $\rho_{\text{write-off}}$: Percentage write-off penalty applied to non-compliant shipments.

### 2. Stochastic Safety Stock ($SS$) & Reorder Point ($ROP$) Engine
Assuming demand during lead time is the convolution of two independent random variables—daily customer demand $D \sim (\overline{D}, \sigma_D^2)$ and replenishment lead time $L \sim (\overline{L}, \sigma_L^2)$—the total variance over lead time is given by:

$$\sigma_{DL}^2 = \overline{L} \cdot \sigma_D^2 + \overline{D}^2 \cdot \sigma_L^2$$

To achieve a targeted Cycle Service Level ($\text{CSL}$), the dynamic safety stock buffer and continuous-review reorder threshold are formulated as:

$$SS = Z \cdot \sqrt{\overline{L} \cdot \sigma_D^2 + \overline{D}^2 \cdot \sigma_L^2}$$

$$ROP = (\overline{D} \cdot \overline{L}) + SS$$

Where:
* $Z = \Phi^{-1}(\text{CSL})$: Inverse standard normal cumulative distribution factor (e.g., $Z = 1.645$ for $95\%$, $Z = 2.326$ for $99\%$).
* $\overline{D}, \sigma_D$: Empirical mean and standard deviation of daily demand.
* $\overline{L}, \sigma_L$: Empirical mean and standard deviation of transit lead time across selected nodes.

---

## 🚀 Key Modules

| Module | Core Logic | Business Impact |
| :--- | :--- | :--- |
| **Executive KPI Strip** | OTIF % & Aggregate Disruption Loss | Delivers immediate visibility into service reliability and total unrecovered vendor penalties. |
| **Lead-Time Variance** | Empirical Histograms & Box Plots | Isolates fat-tail distribution skews and multi-modal transit outliers across freight modes. |
| **Supplier Risk Matrix** | Multi-Variable Risk Space | Maps OTIF reliability against mean delay, sizing nodes by net financial disruption exposure (€). |
| **Inventory Buffer Simulator** | Dual-Variance Propagation | Determines minimum safety stock and ROP required to maintain service targets without inflating inventory carrying cost. |
| **Audit Center** | Automated Exception Filtering | Surfaces non-compliant batches with instant CSV audit ledger extraction. |

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Data Processing & Analytics:** `Pandas`, `NumPy`
* **Visualization Suite:** `Plotly Express`, `Plotly Graph Objects`
* **Application Framework & Deployment:** `Streamlit Cloud`

---

## 📦 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shuklasamyak1/supply-chain-optimizer.git](https://github.com/shuklasamyak1/supply-chain-optimizer.git)
   cd supply-chain-optimizer
