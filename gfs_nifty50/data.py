import os
import pandas as pd

class DataProvider:
    name = "base"
    def history(self, symbol, start, end, resolution="D"):
        raise NotImplementedError

class CsvProvider(DataProvider):
    name = "csv"
    def history(self, symbol, start, end, resolution="D"):
        path=os.getenv("GFS_CSV_DIR","data/raw") + f"/{symbol}.csv"
        df=pd.read_csv(path, parse_dates=["date"])
        return df[(df.date>=start)&(df.date<=end)].copy()

class FyersProvider(DataProvider):
    """
    Credential boundary only. Set FYERS_CLIENT_ID and FYERS_ACCESS_TOKEN.
    Secrets are never stored in the project. The transport mapping is kept
    isolated so the current Fyers SDK/API version can be pinned before use.
    """
    name="fyers"
    def __init__(self, client_id=None, access_token=None):
        self.client_id=client_id or os.getenv("FYERS_CLIENT_ID")
        self.access_token=access_token or os.getenv("FYERS_ACCESS_TOKEN")
        if not self.client_id or not self.access_token:
            raise RuntimeError("Set FYERS_CLIENT_ID and FYERS_ACCESS_TOKEN.")
    def history(self, symbol, start, end, resolution="D"):
        raise NotImplementedError("Configure the pinned Fyers SDK/API transport here.")
