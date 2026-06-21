from subsets_utils import get

flows = ["DF_UNData_UNFCC","DF_UNDATA_COUNTRYDATA","DF_UNData_EnergyBalance","DF_UNDATA_ENERGY"]
for f in flows:
    url = f"https://data.un.org/WS/rest/data/UNSD,{f}/"
    try:
        r = get(url, headers={"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"},
                timeout=(10,180))
        txt = r.text
        lines = txt.splitlines()
        print("="*40)
        print(f, "status", r.status_code, "ctype", r.headers.get("content-type"),
              "bytes", len(r.content), "lines", len(lines))
        if lines:
            print("header:", lines[0][:300])
            if len(lines) > 1:
                print("row1  :", lines[1][:300])
    except Exception as e:
        print("="*40)
        print(f, "ERROR", type(e).__name__, str(e)[:200])
