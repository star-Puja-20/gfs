from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class WalkForwardWindow:
    train_start: pd.Timestamp
    train_end: pd.Timestamp
    test_start: pd.Timestamp
    test_end: pd.Timestamp

def walk_forward_windows(start, end, train_years=10, test_years=1):
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    cursor = start + pd.DateOffset(years=train_years)
    while cursor < end:
        train_start = cursor - pd.DateOffset(years=train_years)
        test_end = min(cursor + pd.DateOffset(years=test_years), end)
        yield WalkForwardWindow(train_start, cursor, cursor, test_end)
        cursor = test_end
