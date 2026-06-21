from datetime import date, timedelta
from subsets_utils import get
import httpx

def windows(start):
    today = date.today()
    cur = start
    while cur <= today:
        we = min(cur + timedelta(days=89), today)
        yield cur.isoformat(), we.isoformat()
        cur = we + timedelta(days=1)

for table in ("A","B"):
    bad = 0
    for ws, we in windows(date(2002,1,2)):
        try:
            r = get(f"https://api.nbp.pl/api/exchangerates/tables/{table}/{ws}/{we}/", params={"format":"json"}, timeout=(10,120))
            if r.status_code == 404:
                continue
            r.raise_for_status()
            for day in r.json():
                for rate in day["rates"]:
                    if "currency" not in rate or "code" not in rate or "mid" not in rate:
                        bad += 1
                        if bad <= 5:
                            print(table, day.get("effectiveDate"), rate)
        except httpx.HTTPStatusError as e:
            print("HTTP", table, ws, we, e.response.status_code)
    print(f"table {table}: {bad} records missing a key")
