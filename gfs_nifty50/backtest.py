from dataclasses import dataclass, asdict
import pandas as pd

@dataclass
class Trade:
    symbol: str; side: str; signal_date: str; entry_date: str
    entry_price: float; qty: int; stop_price: float
    t1_price: float; t2_price: float
    t1_date: str = None; t1_exit_price: float = None
    final_exit_date: str = None; final_exit_price: float = None
    reason: str = None; pnl: float = 0.0; return_pct: float = 0.0

def _long(r):
    return (r.monthly_rsi >= 45 and r.weekly_rsi >= 55 and
            25 <= r.daily_rsi <= 50 and r.daily_rsi > r.daily_rsi_prev and
            (r.close > r.high5 or r.volume >= 1.5*r.vol20) and
            r.volume > 1.2*r.vol20 and r.close > r.ma50)

def _short(r):
    return (r.monthly_rsi <= 55 and r.weekly_rsi <= 45 and
            50 <= r.daily_rsi <= 75 and r.daily_rsi < r.daily_rsi_prev and
            (r.close < r.low5 or r.volume >= 1.5*r.vol20) and
            r.volume > 1.2*r.vol20 and r.close < r.ma50)

def backtest_stock(df, symbol, capital=1_000_000, risk_fraction=.01,
                   fixed_stop_pct=.01, target1_pct=.015, target2_pct=.035,
                   max_hold_days=10, slippage_bps=5):
    x = df.sort_values("date").reset_index(drop=True)
    trades = []
    i = 1
    while i < len(x)-1:
        r = x.iloc[i]
        if any(pd.isna(r[c]) for c in
               ["monthly_rsi","weekly_rsi","daily_rsi","daily_rsi_prev","ma50","vol20","high5","low5"]):
            i += 1; continue
        side = "LONG" if _long(r) else ("SHORT" if _short(r) else None)
        if not side:
            i += 1; continue

        e = x.iloc[i+1]
        entry = float(e.open) * (1 + slippage_bps/10000 if side=="LONG" else 1-slippage_bps/10000)
        stop = entry * (1-.01 if side=="LONG" else 1+.01)
        t1 = entry * (1+target1_pct if side=="LONG" else 1-target1_pct)
        t2 = entry * (1+target2_pct if side=="LONG" else 1-target2_pct)
        qty = int((capital*risk_fraction)/abs(entry-stop))
        if qty <= 0: i += 1; continue

        tr = Trade(symbol, side, str(r.date.date()), str(e.date.date()), entry, qty, stop, t1, t2)
        remaining, realized, t1_done, exit_idx = qty, 0.0, False, None

        for j in range(i+1, min(len(x), i+1+max_hold_days)):
            d = x.iloc[j]; o,h,l,c = map(float,[d.open,d.high,d.low,d.close])
            stop_level = entry if t1_done else stop

            # Conservative priority: stop before target when both occur intraday.
            if side=="LONG":
                if o <= stop_level or l <= stop_level:
                    px = o if o <= stop_level else stop_level
                    realized += remaining*(px-entry)
                    tr.final_exit_date, tr.final_exit_price, tr.reason = str(d.date.date()),px,"STOP_GAP" if o<=stop_level else "STOP"
                    exit_idx=j; break
            else:
                if o >= stop_level or h >= stop_level:
                    px = o if o >= stop_level else stop_level
                    realized += remaining*(entry-px)
                    tr.final_exit_date, tr.final_exit_price, tr.reason = str(d.date.date()),px,"STOP_GAP" if o>=stop_level else "STOP"
                    exit_idx=j; break

            if not t1_done:
                hit = h>=t1 if side=="LONG" else l<=t1
                rsi_hit = d.daily_rsi>70 if side=="LONG" else d.daily_rsi<30
                if hit or rsi_hit:
                    px = t1 if hit else c
                    half = remaining//2
                    if half:
                        realized += half*(px-entry if side=="LONG" else entry-px)
                        remaining -= half
                        tr.t1_date, tr.t1_exit_price = str(d.date.date()),px
                    t1_done=True

            if t1_done and remaining:
                hit = h>=t2 if side=="LONG" else l<=t2
                rsi_hit = d.weekly_rsi>=75 if side=="LONG" else d.weekly_rsi<=25
                ma_hit = c<d.ma5 if side=="LONG" else c>d.ma5
                if hit or rsi_hit or ma_hit:
                    px = t2 if hit else c
                    realized += remaining*(px-entry if side=="LONG" else entry-px)
                    tr.final_exit_date,tr.final_exit_price,tr.reason=str(d.date.date()),px,"T2"
                    exit_idx=j; break

        if exit_idx is None:
            j=min(len(x)-1,i+max_hold_days); d=x.iloc[j]; px=float(d.close)
            realized += remaining*(px-entry if side=="LONG" else entry-px)
            tr.final_exit_date,tr.final_exit_price,tr.reason=str(d.date.date()),px,"TIME"

        tr.pnl=realized; tr.return_pct=realized/(entry*qty)
        trades.append(asdict(tr))
        i=(exit_idx if exit_idx is not None else i+max_hold_days)+1
    return pd.DataFrame(trades)
