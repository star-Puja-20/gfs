from gfs_nifty50.risk import position_size

def test_position_size():
    assert position_size(1_000_000, 2000, 1980, .01) == 500
