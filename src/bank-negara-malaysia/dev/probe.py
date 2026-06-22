import sys, json
sys.path.insert(0, "src")
from utils import _fetch

def show(path, n=2):
    print(f"\n===== {path} =====")
    p = _fetch(path)
    if p is None:
        print("  404 / None"); return
    data = p.get("data"); meta = p.get("meta")
    if meta: print("  meta:", json.dumps(meta)[:300])
    if isinstance(data, list):
        print(f"  list len={len(data)}")
        for r in data[:n]:
            print("  rec:", json.dumps(r)[:400])
    else:
        print("  dict:", json.dumps(data)[:600])

for path in [
    "exchange-rate",
    "exchange-rate/USD/year/2024/month/6",
    "base-rate",
    "opr/year/2024",
    "kijang-emas/year/2024/month/6",
    "interest-rate/year/2024/month/6?product=overall",
    "interest-volume/year/2024/month/6?product=overall",
    "interbank-swap/year/2024/month/6",
    "islamic-interbank-rate/year/2024/month/6",
    "fx-turn-over/year/2024/month/6",
    "kl-usd-reference-rate/year/2024/month/6",
    "usd-interbank-intraday-rate/year/2024/month/6",
    "renminbi-fx-forward-price",
]:
    show(path)
