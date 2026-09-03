import pandas as pd
from gfs_nifty50.indicators import rsi

def test_rsi_bounds():
    s = pd.Series(range(1,60), dtype=float)
    x = rsi(s,14).dropna()
    assert (x >= 0).all() and (x <= 100).all()
