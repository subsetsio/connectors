import sys
sys.path.insert(0, "src")
from nodes.climatic_research_unit import (
    _parse_temperature, _parse_country_file, _get_text,
    TEMP_BASE, _resolve_crucy_dir, _list_per_files,
)
# temperature
t = _get_text(TEMP_BASE + "CRUTEM5.1_gl.txt")
rows = _parse_temperature(t)
print("CRUTEM5 gl rows:", len(rows), "sample:", rows[0], rows[-1])
nn = sum(1 for r in rows if r[2] is not None)
print("non-null values:", nn, "null:", len(rows)-nn)

# country: one file
cd = _resolve_crucy_dir()
print("crucy countries dir:", cd)
files = _list_per_files(cd + "pre/")
print("pre files:", len(files), files[:2])
txt = _get_text(cd + "pre/" + files[1])
country, crows = _parse_country_file(txt, "pre")
print("country:", repr(country), "rows:", len(crows), "sample:", crows[0], crows[-1])
