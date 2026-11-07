"""Streamlit dashboard for the merit-order market model (synthetic data)."""
import sys
from pathlib import Path

# Lets the app find the `market` package inside src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from market.inputs import (
    DEMAND_GW,
    PRICE_CAP_EUR_MWH,
    RENEWABLES_GW,
    TECHNOLOGIES,
)
from market.merit_order import clear_market

st.set_page_config(page_title="Merit Order Lab", layout="wide")
st.title("Merit-order electricity market")
st.caption("Synthetic data, single-zone, inelastic demand. For learning purposes.")

NAMES = [t["name"] for t in TECHNOLOGIES]

# ---- Sidebar: the controls (defaults come from inputs.py) ----
st.sidebar.header("Scenario")
demand_pct = st.sidebar.slider("Demand (% of base)", 70, 130, 100)
ren_pct = st.sidebar.slider("Renewables (% of base)", 0, 200, 100)
coal_cap = st.sidebar.slider("Coal capacity (GW)", 0, 30, 15)
ccg_offer = st.sidebar.slider("CCG offer (EUR/MWh)", 50, 150, 80)
price_cap = st.sidebar.slider("Price cap (EUR/MWh)", 150, 500, int(PRICE_CAP_EUR_MWH))


def hour_inputs(hour):
    """Capacities and offers for one hour, with the sidebar changes applied."""
    capacity = [t["capacity_gw"] for t in TECHNOLOGIES]
    offers = [t["offer_eur_mwh"] for t in TECHNOLOGIES]
    capacity[NAMES.index("Renewables")] = RENEWABLES_GW[hour] * ren_pct / 100
    capacity[NAMES.index("Coal")] = coal_cap
    offers[NAMES.index("CCG")] = ccg_offer
    demand = DEMAND_GW[hour] * demand_pct / 100
    return capacity, offers, demand


rows = []
for hour in range(24):
    capacity, offers, demand = hour_inputs(hour)
    result = clear_market(capacity, offers, demand, price_cap)
    idx = result["marginal_index"]
    rows.append(
        {
            "hour": hour,
            "demand_gw": round(demand, 1),
            "price_eur_mwh": result["price"],
            "marginal": NAMES[idx] if idx is not None else "SHORTAGE",
            "unserved_gw": round(result["unserved"], 1),
        }
    )
df = pd.DataFrame(rows)

# ---- Summary numbers ----
c1, c2, c3 = st.columns(3)
c1.metric("Average price (EUR/MWh)", f"{df['price_eur_mwh'].mean():.1f}")
c2.metric("Max price (EUR/MWh)", f"{df['price_eur_mwh'].max():.0f}")
c3.metric("Shortage hours", int((df["unserved_gw"] > 0).sum()))

# ---- Price over the day ----
st.subheader("Clearing price by hour")
st.line_chart(df.set_index("hour")["price_eur_mwh"])

# ---- Merit order staircase for one hour ----
st.subheader("Merit order for one hour")
hour = st.slider("Hour of the day", 0, 23, 18)
capacity, offers, demand = hour_inputs(hour)
result = clear_market(capacity, offers, demand, price_cap)

order = sorted(range(len(offers)), key=lambda i: offers[i])
x, y, cum = [0.0], [offers[order[0]]], 0.0
for i in order:
    cum += capacity[i]
    x.append(cum)
    y.append(offers[i])

fig, ax = plt.subplots(figsize=(8, 4))
ax.step(x, y, where="pre")
ax.axvline(demand, linestyle="--", color="red", label=f"Demand {demand:.1f} GW")
ax.set_xlabel("Cumulative capacity (GW)")
ax.set_ylabel("Offer (EUR/MWh)")
ax.set_title(f"Hour {hour}: price {result['price']:.0f} EUR/MWh")
ax.legend()
st.pyplot(fig)

with st.expander("Hourly results table"):
    st.dataframe(df, hide_index=True)