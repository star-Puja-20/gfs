import numpy as np
import pandas as pd

def profit_factor(pnl):
    pnl = pd.Series(pnl)
    gross_profit = pnl[pnl > 0].sum()
    gross_loss = -pnl[pnl < 0].sum()
    return np.inf if gross_loss == 0 and gross_profit > 0 else (gross_profit/gross_loss if gross_loss else 0)

def max_drawdown(equity):
    e = pd.Series(equity).astype(float)
    peak = e.cummax()
    return ((e/peak)-1).min()

def trade_metrics(trades):
    if trades.empty:
        return {"trades":0, "win_rate":0, "profit_factor":0, "expectancy_r":0,
                "avg_winner":0, "avg_loser":0, "max_drawdown":0}
    wins = trades[trades.pnl > 0]
    losses = trades[trades.pnl < 0]
    return {
        "trades": len(trades),
        "win_rate": len(wins)/len(trades),
        "profit_factor": profit_factor(trades.pnl),
        "expectancy_r": trades.r_multiple.mean(),
        "avg_winner": wins.pnl.mean() if len(wins) else 0,
        "avg_loser": losses.pnl.mean() if len(losses) else 0,
        "max_drawdown": max_drawdown(trades.pnl.cumsum())
    }
