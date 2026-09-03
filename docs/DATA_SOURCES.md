# Data source contract

The engine deliberately does not hard-code a vendor.

Provide reliable data for:

1. Daily OHLCV for all NIFTY 50 constituents.
2. Point-in-time NIFTY 50 membership.
3. NIFTY 50 benchmark OHLCV.
4. Corporate actions.
5. Sector classifications.
6. Optional India VIX.
7. Optional earnings/event calendar.

A Fyers/NSE-compatible adapter can be added under `gfs_nifty50/providers/`.

Do not use today's constituents for a long historical backtest and call the result
unbiased. The GFS specification explicitly requires point-in-time membership when
available.
