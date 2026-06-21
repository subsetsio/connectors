from subsets_utils import get
r = get("https://storage.googleapis.com/global-surface-water-stats/gaul2-all-2018.csv", timeout=(10,300))
data = r.content
# find a line with bytes >127
import re
lines = data.split(b"\n")
print("total bytes", len(data))
shown=0
for ln in lines:
    if any(b>127 for b in ln):
        # try decodes
        try: u8 = ln.decode("utf-8")
        except Exception as e: u8 = f"<utf8 fail: {e}>"
        lat = ln.decode("latin-1")
        cp = ln.decode("cp1252", errors="replace")
        # only show ones where utf-8 fails or has replacement
        if "<utf8 fail" in str(u8) or "�" in (u8 if isinstance(u8,str) else ""):
            print("RAW   :", ln[:120])
            print("utf8  :", u8[:120] if isinstance(u8,str) else u8)
            print("latin1:", lat[:120])
            print("cp1252:", cp[:120])
            print("---")
            shown+=1
            if shown>=6: break
