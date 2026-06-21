import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.environ.pop("CI", None)
import nodes.bts as m

# prezip: discover prefix, download one month, verify batch_key + obs fields
meta = m._page_meta("FGJ")
print("FGJ meta:", meta["period_type"], "years", meta["years"][0], meta["years"][-1], "geo", meta["has_geo"])
prefix = m._discover_prezip_prefix("FGJ", meta)
print("FGJ prefix:", prefix)
content = m._download_prezip(prefix, 2024, "3")
print("FGJ 2024-3 zip bytes:", len(content) if content else None)
n = m._write_batch("bts-fgj-2024-03", content, *m._obs_fields(meta, 2024, "3"))
print("FGJ 2024-03 rows:", n, "batch_key", m._batch_key(meta,2024,"3"), "obs", m._obs_fields(meta,2024,"3"))

# quarterly custom: FIH one quarter
meta2 = m._page_meta("FIH")
print("FIH meta:", meta2["period_type"], "geo", meta2["has_geo"])
c2 = m._download_custom("FIH", meta2, 2023, "2")
print("FIH 2023 Q2 zip bytes:", len(c2) if c2 else None)
n2 = m._write_batch("bts-fih-2023-Q2", c2, *m._obs_fields(meta2, 2023, "2"))
print("FIH 2023-Q2 rows:", n2, "batch_key", m._batch_key(meta2,2023,"2"), "obs", m._obs_fields(meta2,2023,"2"))
