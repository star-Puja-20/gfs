import numpy as np

def minmax(values, higher_is_better=True):
    vals = np.asarray(values, dtype=float)
    if np.all(~np.isfinite(vals)): return np.zeros_like(vals)
    finite = vals[np.isfinite(vals)]
    lo, hi = finite.min(), finite.max()
    if hi == lo: out = np.ones_like(vals)*50
    else: out = (vals-lo)/(hi-lo)*100
    return out if higher_is_better else 100-out

def quality_score(rows):
    # Baseline weights from GFS-NIFTY50 v2.0. Input must already contain
    # out-of-sample and robustness metrics; missing metrics are neutral, not fabricated.
    specs = [
        ("oos_expectancy", .20, True),
        ("profit_factor", .15, True),
        ("calmar", .15, True),
        ("sortino", .10, True),
        ("walk_forward_score", .15, True),
        ("expectancy_r", .10, True),
        ("trade_count", .05, True),
        ("cost_robustness", .05, True),
        ("liquidity_score", .05, True),
    ]
    scores = []
    for col, weight, high in specs:
        vals = [r.get(col, np.nan) for r in rows]
        s = minmax(vals, high)
        scores.append(s*weight)
    return np.sum(scores, axis=0)
