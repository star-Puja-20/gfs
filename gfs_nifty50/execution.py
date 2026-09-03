def apply_slippage(price, side, slippage_bps):
    # Positive cost to the trader in either direction.
    factor = 1 + slippage_bps / 10000 if side == "BUY" else 1 - slippage_bps / 10000
    return price * factor

def transaction_cost(notional, bps):
    return abs(notional) * bps / 10000
