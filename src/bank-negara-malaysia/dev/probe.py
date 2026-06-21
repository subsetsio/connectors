import json
from subsets_utils import get

H = {"Accept": "application/vnd.BNM.API.v1+json"}
B = "https://api.bnm.gov.my/public"


def show(path, label):
    r = get(f"{B}/{path}", headers=H, timeout=(10, 60))
    print(f"\n=== {label} ({path}) [{r.status_code}] ===")
    if r.status_code != 200:
        print(r.text[:200]); return
    d = r.json()
    data = d.get("data")
    print("meta:", d.get("meta"))
    if isinstance(data, list):
        print("list len:", len(data))
        print("first:", json.dumps(data[0]) if data else None)
    else:
        print("dict:", json.dumps(data))


show("exchange-rate/USD/year/2024/month/3", "exchange-rate USD month")
show("interest-rate/year/2024/month/3", "interest-rate month")
show("kijang-emas/year/2024/month/3", "kijang-emas month")
show("islamic-interbank-rate/year/2024/month/3", "islamic month")
show("interbank-swap/year/2024/month/3", "interbank-swap month")
show("fx-turn-over/year/2024/month/3", "fx-turn-over month")
show("usd-interbank-intraday-rate/year/2024/month/3", "usd intraday month")
show("opr/year/2020", "opr year")
