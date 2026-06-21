from subsets_utils import get

REMAIN = [
    "060863044a0f4e4b8eec84c85e3eedf6",
    "0a50d4048b27441a84e8ff98e71d023e",
    "0f200a12da104da3936bbf291b394fbc",
    "11fd91ff08f04c618b2f87bec2a1a420",
    "397650f2bdfe40a7babffbcae91ae639",
    "4e4a998fa9c340d5804fd41f0b3a35bc",
    "4fa3ff8b968d481f8cb9799b07086ca2",
    "5b4a50c56d414167b709e3fa93829063",
    "6b93d3b1a4b841f586f07406eb621b62",
    "bc1cfb5ef50a43a9b60e25c11c32255b",
    "d604f91a049a42d0bb7cabf17fdde9ff",
    "ee6b2c4f8fdb40edad85e682490509b9",
]
for iid in REMAIN:
    item = get(f"https://www.arcgis.com/sharing/rest/content/items/{iid}",
               params={"f": "json"}, timeout=(10, 60)).json()
    svc = item.get("url")
    root = get(svc, params={"f": "json"}, timeout=(10, 60)).json() if svc else {}
    layers = root.get("layers") or []
    tables = root.get("tables") or []
    lid = (layers or tables)[0]["id"] if (layers or tables) else None
    cnt = None
    nfields = None
    if svc and lid is not None:
        cnt = get(f"{svc}/{lid}/query",
                  params={"where": "1=1", "returnCountOnly": "true", "f": "json"},
                  timeout=(10, 60)).json().get("count")
        meta = get(f"{svc}/{lid}", params={"f": "json"}, timeout=(10, 60)).json()
        nfields = len(meta.get("fields") or [])
    print(f"{iid} | url={'Y' if svc else 'N'} | layer={lid} | rows={cnt} | fields={nfields} | {item.get('title')}")
