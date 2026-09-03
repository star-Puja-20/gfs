import argparse
from pathlib import Path
import pandas as pd
import yaml
from .data import load_ohlcv
from .indicators import add_daily_indicators, add_higher_timeframe_rsi
from .signals import generate_signals
from .backtest import backtest_stock
from .metrics import trade_metrics

def prepared_data(path, cfg):
    d = load_ohlcv(path)
    d = add_daily_indicators(d, cfg["strategy"])
    d = add_higher_timeframe_rsi(d, cfg["strategy"])
    return generate_signals(d, cfg["strategy"])

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("backtest","rank","signals"):
        s = sub.add_parser(name)
        s.add_argument("--config", required=True)
        s.add_argument("--data", default="data/sample/nifty50_daily.csv")
        s.add_argument("--output", default="outputs")
    a = p.parse_args()
    cfg = yaml.safe_load(Path(a.config).read_text())
    d = prepared_data(a.data, cfg)

    if a.cmd == "signals":
        latest = d.sort_values("date").groupby("symbol").tail(1)
        cols = ["symbol","date","monthly_rsi","weekly_rsi","rsi_d","volume_ratio","signal"]
        Path(a.output).mkdir(exist_ok=True)
        latest[cols].to_csv(Path(a.output)/"current_signals.csv", index=False)
        print(latest[cols].to_string(index=False))

    elif a.cmd == "backtest":
        rows = []
        for symbol in sorted(d.symbol.unique()):
            t, final_eq = backtest_stock(d, symbol, 1_000_000, cfg["strategy"],
                                         cfg["execution"]["slippage_bps"])
            m = trade_metrics(t)
            m["symbol"], m["final_equity"] = symbol, final_eq
            rows.append(m)
        out = pd.DataFrame(rows)
        Path(a.output).mkdir(exist_ok=True)
        out.to_csv(Path(a.output)/"stock_backtest_metrics.csv", index=False)
        print(out.sort_values("profit_factor", ascending=False).to_string(index=False))

    elif a.cmd == "rank":
        print("Ranking requires validated stock-level OOS/walk-forward metrics. "
              "Use the backtest output plus validation results; no synthetic ranking is produced.")

if __name__ == "__main__":
    main()
