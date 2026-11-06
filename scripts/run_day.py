"""Run the merit-order market for each hour of a day and print the results."""
import sys
from pathlib import Path

# Lets the script find the `market` package inside src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pandas as pd

from market.inputs import (
    DEMAND_GW,
    PRICE_CAP_EUR_MWH,
    RENEWABLES_GW,
    TECHNOLOGIES,
)
from market.merit_order import clear_market


def main():
    names = [t["name"] for t in TECHNOLOGIES]
    offers = [t["offer_eur_mwh"] for t in TECHNOLOGIES]

    rows = []
    for hour in range(24):
        capacity = [t["capacity_gw"] for t in TECHNOLOGIES]
        capacity[0] = RENEWABLES_GW[hour]  # the first block is Renewables
        result = clear_market(capacity, offers, DEMAND_GW[hour], PRICE_CAP_EUR_MWH)

        idx = result["marginal_index"]
        marginal = names[idx] if idx is not None else "SHORTAGE"
        rows.append(
            {
                "hour": hour,
                "demand_gw": DEMAND_GW[hour],
                "renewables_gw": RENEWABLES_GW[hour],
                "price_eur_mwh": result["price"],
                "marginal": marginal,
                "unserved_gw": result["unserved"],
            }
        )

    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()