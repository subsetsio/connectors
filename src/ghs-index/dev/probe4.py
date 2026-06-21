from subsets_utils import get
origin = "https://ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv"
api = get("https://archive.org/wayback/available", params={"url": origin}, timeout=(10.0,120.0)).json()
snap = api["archived_snapshots"]["closest"]
print("snapshot:", snap["timestamp"], snap["status"], snap["available"])
ts = snap["timestamp"]
raw_url = f"https://web.archive.org/web/{ts}id_/{origin}"
r = get(raw_url, timeout=(10.0,120.0))
print("raw status:", r.status_code, "len:", len(r.content))
text = r.content.decode("utf-8-sig")
print("first header field:", repr(text.split(",")[0]))
print("n lines:", text.count(chr(10)))
