import sys
sys.path.insert(0, "src")
from nodes.dartmouth_atlas_of_health_care import _fetch_zip_rows, _normalize_topic_row, _geo_level
from constants import BASE

# topic file (modern, has race/gender)
name, rows = _fetch_zip_rows(BASE + "downloads/research_files/hrr_eolmedpar_dead6699ffs.csv.zip")
print("eolmedpar modern:", name, len(rows), "rows; keys:", sorted(rows[0].keys())[:6], "...")
nr = _normalize_topic_row(rows[0], _geo_level(name))
print("normalized sample:", {k: nr[k] for k in ("geo_level","geo_code","year","measure_code","adjusted_rate","oe_ratio","race")})

# legacy file (fewer cols)
name2, rows2 = _fetch_zip_rows(BASE + "downloads/research_files/hrr_meddischarges_1992_2007.csv.zip")
nr2 = _normalize_topic_row(rows2[0], _geo_level(name2))
print("meddischarges legacy normalized:", {k: nr2[k] for k in ("geo_level","year","measure_code","adjusted_rate","oe_ratio")})

# hedis (o_e_ratio + lowercase adjusted_rate)
name3, rows3 = _fetch_zip_rows(BASE + "downloads/research_files/hrr_hedis_6575ffs.csv.zip")
nr3 = _normalize_topic_row(rows3[0], _geo_level(name3))
print("hedis normalized:", {k: nr3[k] for k in ("year","measure_code","adjusted_rate","oe_ratio")})

# crosswalk
name4, rows4 = _fetch_zip_rows(BASE + "downloads/geography/ZipHsaHrr19.csv.zip")
print("crosswalk:", name4, len(rows4), "keys:", sorted(rows4[0].keys()))
