import sys, gzip
sys.path.insert(0,"src")
from datetime import date, timedelta
from nodes.statcast import STATCAST_WINDOW_DAYS, STATCAST_ROW_CAP
from utils import _fetch_csv_text

# probe a few in-season windows (2024) — confirm endpoint returns CSV under cap
cur = date(2024,7,1)
for _ in range(3):
    win_end = cur + timedelta(days=STATCAST_WINDOW_DAYS-1)
    url=("https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details"
         f"&player_type=pitcher&game_date_gt={cur.isoformat()}&game_date_lt={win_end.isoformat()}")
    t=_fetch_csv_text(url)
    if t is None:
        print(cur, "-> None"); cur=win_end+timedelta(days=1); continue
    if t and t[0]=="﻿": t=t[1:]
    n=max(0,len(t.splitlines())-1)
    print(cur,"->",win_end, "rows=",n, "under_cap=", n<STATCAST_ROW_CAP)
    cur=win_end+timedelta(days=1)
