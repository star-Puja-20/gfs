import pandas as pd

def generate_signals(df, cfg):
    x = df.copy()
    g = x.groupby("symbol", group_keys=False)
    x["rsi_d_prev"] = g["rsi_d"].shift(1)

    long_cond = (
        x["monthly_rsi"].ge(cfg["monthly_long_min"]) &
        x["monthly_rsi"].le(cfg["monthly_long_max"]) &
        x["weekly_rsi"].ge(cfg["weekly_long_min"]) &
        x["weekly_rsi"].le(cfg["weekly_long_max"]) &
        x["rsi_d"].between(cfg["daily_long_min"], cfg["daily_long_max"]) &
        x["rsi_d"].gt(x["rsi_d_prev"]) &
        x["close"].gt(x["prev5_high"]) &
        x["volume_ratio"].gt(cfg["volume_ratio"]) &
        x["close"].gt(x["ma50"])
    )

    short_cond = (
        x["monthly_rsi"].le(cfg["monthly_short_max"]) &
        x["monthly_rsi"].ge(cfg["monthly_short_min"]) &
        x["weekly_rsi"].le(cfg["weekly_short_max"]) &
        x["weekly_rsi"].ge(cfg["weekly_short_min"]) &
        x["rsi_d"].between(cfg["daily_short_min"], cfg["daily_short_max"]) &
        x["rsi_d"].lt(x["rsi_d_prev"]) &
        x["close"].lt(x["prev5_low"]) &
        x["volume_ratio"].gt(cfg["volume_ratio"]) &
        x["close"].lt(x["ma50"])
    )

    x["signal"] = "NONE"
    x.loc[long_cond, "signal"] = "LONG"
    x.loc[short_cond, "signal"] = "SHORT"
    return x
