import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_orders = 2500

suppliers = ['Supplier A (Germany)', 'Supplier B (China)', 'Supplier C (USA)', 'Supplier D (India)', 'Supplier E (Vietnam)']
shipping_modes = ['Air Freight', 'Ocean Cargo', 'Express Courier', 'Rail Freight']
product_categories = ['Industrial Components', 'Raw Materials', 'Electronics', 'Heavy Machinery']

start_date = datetime(2025, 1, 1)
order_dates = [start_date + timedelta(days=int(d)) for d in np.random.randint(0, 365, n_orders)]

data = {
    'order_id': [f"ORD-{10000 + i}" for i in range(n_orders)],
    'order_date': order_dates,
    'supplier': np.random.choice(suppliers, n_orders, p=[0.25, 0.30, 0.15, 0.20, 0.10]),
    'shipping_mode': np.random.choice(shipping_modes, n_orders, p=[0.30, 0.40, 0.20, 0.10]),
    'product_category': np.random.choice(product_categories, n_orders),
    'order_value_eur': np.random.lognormal(mean=8.5, sigma=0.8, size=n_orders).round(2),
    'promised_lead_time_days': np.random.choice([7, 14, 21, 30, 45], n_orders)
}

df = pd.DataFrame(data)

base_delay = np.random.exponential(scale=3.5, size=n_orders)
df['actual_lead_time_days'] = df['promised_lead_time_days'] + np.where(
    np.random.rand(n_orders) > 0.35, 
    base_delay.round(0), 
    -np.random.randint(0, 3, n_orders)
)
df['actual_lead_time_days'] = df['actual_lead_time_days'].clip(lower=2).astype(int)

df['is_delayed'] = df['actual_lead_time_days'] > df['promised_lead_time_days']
df['delay_days'] = np.maximum(0, df['actual_lead_time_days'] - df['promised_lead_time_days'])
df['is_defective'] = np.random.choice([True, False], n_orders, p=[0.04, 0.96])
df['is_otif'] = (~df['is_delayed']) & (~df['is_defective'])

df.to_csv('supply_chain_data.csv', index=False)
print("supply_chain_data.csv generated successfully.")