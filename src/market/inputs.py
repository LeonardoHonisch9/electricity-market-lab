


TECHNOLOGIES = [
    {"name": "Renewables", "capacity_gw": 20, "offer_eur_mwh": 0},
    {"name": "Nuclear",    "capacity_gw": 10, "offer_eur_mwh": 10},
    {"name": "Coal",       "capacity_gw": 15, "offer_eur_mwh": 50},
    {"name": "CCG",        "capacity_gw": 20, "offer_eur_mwh": 80},
    {"name": "P Gas",      "capacity_gw": 5,  "offer_eur_mwh": 150},
]


PRICE_CAP_EUR_MWH = 250


EXAMPLE_DEMAND_GW = 50

# --- Hourly profiles (synthetic, for illustration only) ---
# Index = hour of the day (0 to 23).

# Demand (GW): low at night, morning ramp, small midday dip, evening peak.
DEMAND_GW = [
    36, 34, 33, 33, 35, 40,   # 00-05
    47, 53, 55, 52, 49, 47,   # 06-11
    46, 46, 47, 49, 53, 56,   # 12-17
    61, 58, 53, 48, 42, 38,   # 18-23
]

# Available renewable capacity (GW): small at night (wind), peak at midday (solar).
RENEWABLES_GW = [
    8, 8, 7, 7, 7, 8,         # 00-05
    10, 14, 20, 26, 30, 32,   # 06-11
    32, 31, 29, 25, 18, 14,   # 12-17
    10, 10, 10, 8, 8, 8,      # 18-23
]