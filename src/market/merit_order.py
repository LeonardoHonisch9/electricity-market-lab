"""Merit-order mechanism: how a uniform-price auction clears.

Logic only. This module never imports inputs.py: all data arrives
as function arguments.
"""


def clear_market(capacity, offers, demand, price_cap):
    """Clear a single-hour uniform-price auction.

    Parameters
    ----------
    capacity : sequence of float
        Available power per block (GW).
    offers : sequence of float
        Offer per block (EUR/MWh), same order and length as `capacity`.
    demand : float
        Inelastic demand for the hour (GW), >= 0.
    price_cap : float
        Price used when demand exceeds total capacity (EUR/MWh).

    Returns
    -------
    dict with keys:
        price : float
            Offer of the marginal block; `price_cap` if demand > total capacity.
        dispatched : list of float
            GW used per block, in the ORIGINAL input order.
        unserved : float
            Demand not covered (GW), 0 if fully served.
        marginal_index : int or None
            Index (original order) of the block that sets the price,
            None when demand exceeds total capacity.

    Conventions
    -----------
    - Blocks are sorted by offer internally (stable sort: ties keep input order).
    - Marginal block = first block, in merit order, whose cumulative capacity
      covers demand. Demand exactly equal to a cumulative value belongs to that block.
    - Demand 0: price = lowest offer, marginal block = cheapest block.
    - Raises ValueError if lengths differ or any capacity/demand is negative.
    """
    # 1. Validate inputs
    if len(capacity) != len(offers):
        raise ValueError("capacity and offers must have the same length")
    if demand < 0 or any(c < 0 for c in capacity):
        raise ValueError("demand and capacities must be non-negative")

    # 2. Block positions sorted by offer (cheapest first).
    order = sorted(range(len(offers)), key=lambda i: offers[i])

    # 3. Walk the blocks from cheapest to most expensive
    dispatched = [0.0] * len(capacity)
    remaining = demand        
    cumulative = 0.0          
    marginal_index = None

    for i in order:
        used = min(capacity[i], remaining)   
        dispatched[i] = used
        remaining -= used
        cumulative += capacity[i]

        # 4. The first block whose cumulative capacity covers demand is marginal
        if marginal_index is None and cumulative >= demand:
            marginal_index = i

    # 5. Price and unserved demand
    if marginal_index is None:      
        price = price_cap
        unserved = remaining
    else:
        price = offers[marginal_index]
        unserved = 0.0

    # 6. dispatched is already in the original order
    return {
        "price": price,
        "dispatched": dispatched,
        "unserved": unserved,
        "marginal_index": marginal_index,
    }