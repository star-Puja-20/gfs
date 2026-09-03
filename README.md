# GFS NIFTY 50 Research System

A reproducible Python research/backtesting implementation of the GFS-NIFTY50 v2.0 specification.

## Architecture

Data → Universe → Indicators → GFS Signals → Execution Model → Position Sizing →
Portfolio Construction → Backtest → Validation → Stock Ranking → Current Signals → Risk Report

## Important

This repository implements the research engine. It does **not** manufacture performance results.
A real backtest requires reliable historical OHLCV, point-in-time NIFTY 50 membership,
corporate actions, and cost/slippage assumptions.

The specification requires monthly/weekly/daily RSI, 5-session breakout/breakdown,
volume confirmation, NIFTY regime filtering, stock-level quality ranking, walk-forward
validation, survivorship-bias testing, portfolio risk controls, and realistic execution.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m gfs_nifty50.cli backtest --config configs/default.yaml
python -m gfs_nifty50.cli rank --config configs/default.yaml
python -m gfs_nifty50.cli signals --config configs/default.yaml
```

For an initial local smoke test, use the sample CSV data in `data/sample/`.

## Data contract

Daily stock CSV:

`date,symbol,open,high,low,close,volume`

Benchmark CSV:

`date,symbol,open,high,low,close,volume`

Dates must be timezone-naive trading dates. Prices should be adjusted consistently for
corporate actions.

## Validation discipline

- Higher-timeframe indicators use only completed weekly/monthly candles.
- Historical universe membership is point-in-time when available.
- Signal decisions cannot access future rows.
- Execution defaults to next-session open plus configured slippage.
- Gross and net P&L are reported separately.
- Parameters are selected on training data only.
- Final test periods remain untouched until evaluation.
