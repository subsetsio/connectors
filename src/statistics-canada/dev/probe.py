import io, zipfile, json
from subsets_utils import get

def resolve(pid):
    r = get(f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en", timeout=(10,120))
    r.raise_for_status()
    j = r.json()
    return j

# probe a few candidate ids to find a small one
for pid in ["10100002","36100434","17100005"]:
    j = resolve(pid)
    print(pid, "resolve ->", j)
    url = j["object"] if isinstance(j, dict) else j[0]["object"]
    rz = get(url, timeout=(10,300))
    print("  zip bytes:", len(rz.content))
    zf = zipfile.ZipFile(io.BytesIO(rz.content))
    print("  members:", [(n.filename, n.file_size) for n in zf.infolist()])
    member = f"{pid}.csv"
    with zf.open(member) as f:
        head = f.read(3000)
    text = head.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    print("  HEADER:", lines[0])
    print("  ROW1  :", lines[1] if len(lines)>1 else "<none>")
    print("="*80)
    break  # just the first one that works
