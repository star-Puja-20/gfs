import math

def position_size(equity, entry, stop, risk_fraction=.01):
    risk_budget = equity * risk_fraction
    risk_per_share = abs(entry - stop)
    if risk_per_share <= 0:
        return 0
    return math.floor(risk_budget / risk_per_share)

def portfolio_risk(open_positions):
    return sum(p["risk_fraction"] for p in open_positions)

def sector_count(open_positions, sector):
    return sum(p["sector"] == sector for p in open_positions)
