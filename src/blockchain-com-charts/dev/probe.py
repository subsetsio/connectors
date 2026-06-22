from subsets_utils import get
for slug in ["market-price", "mempool-count", "total-bitcoins"]:
    r = get("https://api.blockchain.info/charts/" + slug,
            params={"timespan": "all", "sampled": "false", "format": "json"}, timeout=(10,120))
    d = r.json()
    v = d["values"]
    print(slug, "status=", d["status"], "unit=", d["unit"], "period=", d["period"],
          "n=", len(v), "first=", v[0], "last=", v[-1], "xtype=", type(v[0]["x"]).__name__, "ytype=", type(v[0]["y"]).__name__)
