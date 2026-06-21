from subsets_utils import get
from nodes.silso import _fetch_text, _parse, SERIES

for eid in ["daily-total", "yearly-total"]:
    url, cols = SERIES[eid]
    chunked = _fetch_text(url)
    plain = get(url, headers={"Accept-Encoding":"identity"}, timeout=(30.0,180.0)).text
    print(f"{eid}: chunked_len={len(chunked)} plain_len={len(plain)} match={chunked==plain}")
    t = _parse(chunked, cols)
    print(f"   parsed rows={t.num_rows}")
