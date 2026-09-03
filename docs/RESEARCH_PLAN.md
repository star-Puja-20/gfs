# GFS NIFTY 50 v2.1

Implemented:
- NIFTY 50 constituent-by-constituent GFS processing.
- Completed weekly/monthly RSI alignment; no incomplete HTF candle.
- Close-of-day signal -> next-session-open execution.
- T1 50% exit, breakeven stop, T2/hard exits and max holding period.
- Gap-through-stop handling and conservative same-bar stop priority.
- Risk-based quantity sizing.
- Fyers provider boundary with environment-only credentials.

Required before live/profitability claims:
1. Pin and implement the current Fyers API/SDK transport.
2. Load point-in-time NIFTY 50 membership.
3. Add NIFTY 50 benchmark/VIX data.
4. Add portfolio-level 5-position, sector and correlation controls.
5. Add Indian brokerage/tax/impact cost model.
6. Add walk-forward/OOS, Monte Carlo and parameter sensitivity.
7. Independently validate signals/exits against reference calculations.
