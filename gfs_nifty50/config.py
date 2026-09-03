from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass(frozen=True)
class StrategyConfig:
    rsi_period: int = 14
    monthly_long_min: float = 45
    monthly_long_max: float = 75
    weekly_long_min: float = 55
    weekly_long_max: float = 80
    daily_long_min: float = 25
    daily_long_max: float = 50
    monthly_short_max: float = 55
    monthly_short_min: float = 20
    weekly_short_max: float = 45
    weekly_short_min: float = 20
    daily_short_min: float = 50
    daily_short_max: float = 75
    breakout_lookback: int = 5
    volume_lookback: int = 20
    volume_ratio: float = 1.2
    regime_ma: int = 50
    target1_pct: float = .015
    target2_min_pct: float = .03
    target2_max_pct: float = .04

@dataclass(frozen=True)
class RiskConfig:
    risk_per_trade: float = .01
    max_portfolio_risk: float = .04
    max_positions: int = 5
    max_sector_positions: int = 2

@dataclass(frozen=True)
class ExecutionConfig:
    slippage_bps: float = 10

def load_config(path):
    raw = yaml.safe_load(Path(path).read_text())
    return raw
