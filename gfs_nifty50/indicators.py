import pandas as pd
import numpy as np

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    ag = gain.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    al = loss.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    rs = ag / al.replace(0, np.nan)
    return 100 - 100/(1+rs)

def atr(df, period=14):
    pc = df["close"].shift(1)
    tr = pd.concat([
        df["high"]-df["low"],
        (df["high"]-pc).abs(),
        (df["low"]-pc).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, adjust=False, min_periods=period).mean()

def sma(s, period):
    return s.rolling(period, min_periods=period).mean()

def _htf(df, rule):
    return (df.set_index("date")
              .resample(rule, label="right", closed="right")
              .agg({"open":"first","high":"max","low":"min","close":"last","volume":"sum"})
              .dropna().reset_index())

def completed_htf_rsi(daily, rule, period=14):
    x = daily[["date","open","high","low","close","volume"]].copy()
    x["date"] = pd.to_datetime(x["date"]).dt.normalize()
    h = _htf(x, rule)
    h["rsi"] = rsi(h["close"], period)
    h["available_from"] = h["date"] + pd.Timedelta(days=1)
    return pd.merge_asof(
        x[["date"]].sort_values("date"),
        h[["available_from","rsi"]].sort_values("available_from"),
        left_on="date", right_on="available_from", direction="backward"
    )["rsi"].set_axis(daily.index)

def add_gfs_indicators(df):
    x = df.copy()
    x["date"] = pd.to_datetime(x["date"]).dt.normalize()
    x = x.sort_values("date").reset_index(drop=True)
    x["daily_rsi"] = rsi(x.close, 14)
    x["daily_rsi_prev"] = x.daily_rsi.shift(1)
    x["daily_atr"] = atr(x, 14)
    x["ma5"] = sma(x.close, 5)
    x["ma50"] = sma(x.close, 50)
    x["vol20"] = x.volume.rolling(20, min_periods=20).mean()
    x["high5"] = x.high.rolling(5, min_periods=5).max().shift(1)
    x["low5"] = x.low.rolling(5, min_periods=5).min().shift(1)
    x["weekly_rsi"] = completed_htf_rsi(x, "W-FRI", 14)
    x["monthly_rsi"] = completed_htf_rsi(x, "ME", 14)
    return x
