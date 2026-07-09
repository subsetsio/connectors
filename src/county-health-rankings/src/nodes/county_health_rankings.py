"""County Health Rankings & Roadmaps (CHR&R) connector.

Source: University of Wisconsin Population Health Institute (RWJF-funded).
Mechanism: bulk CSV files under www.countyhealthrankings.org. Stateless full
re-pull each run — the whole corpus is a handful of CSVs fetched in a couple of
minutes, and re-pulling picks up revisions/late corrections for free.

Two published subsets:

  * trends   — the single long-format trends CSV (chr_trends_csv_<YEAR>.csv,
               cumulative back to 1997). One row per (yearspan, measure, county).
  * analytic — the per-release-year wide analytic files (analytic_data<YEAR>.csv,
               2010-present), UNPIVOTED here to a uniform long schema:
               one row per (release_year, fips, measure). The analytic files
               carry a TWO-row header (human names, then stable variable codes
               like `v001_rawvalue`); we key measures off the stable v-codes so
               the measure_id is consistent across years and joins to
               trends.measure_id. Only the OVERALL value/CI columns are kept
               (race-stratified columns are dropped). Different years expose
               different column sets, so unpivoting in-process (rather than as
               raw parquet) is what lets every year union to one schema.

File URLs are DISCOVERED from the documentation pages each run (filenames carry
irregular version suffixes year to year), never hardcoded.
"""

import csv
import io
import re

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import NodeSpec, get, transient_retry, raw_parquet_writer

HOST = "https://www.countyhealthrankings.org"
DOC_PAGES = [
    f"{HOST}/health-data/methodology-and-sources/data-documentation",
    f"{HOST}/health-data/methodology-and-sources/data-documentation/national-data-documentation-2010-2023",
]

_BATCH_ROWS = 200_000

TRENDS_SCHEMA = pa.schema([
    ("yearspan", pa.string()),
    ("measure_name", pa.string()),
    ("measure_id", pa.int64()),
    ("state_fips", pa.string()),
    ("county_fips", pa.string()),
    ("fips", pa.string()),
    ("county", pa.string()),
    ("state", pa.string()),
    ("numerator", pa.float64()),
    ("denominator", pa.float64()),
    ("raw_value", pa.float64()),
    ("ci_low", pa.float64()),
    ("ci_high", pa.float64()),
    ("release_year", pa.int64()),
])

ANALYTIC_SCHEMA = pa.schema([
    ("release_year", pa.int64()),
    ("state_fips", pa.string()),
    ("county_fips", pa.string()),
    ("fips", pa.string()),
    ("state", pa.string()),
    ("county", pa.string()),
    ("measure_id", pa.int64()),
    ("measure_name", pa.string()),
    ("raw_value", pa.float64()),
    ("numerator", pa.float64()),
    ("denominator", pa.float64()),
    ("ci_low", pa.float64()),
    ("ci_high", pa.float64()),
])

MEASURES_SCHEMA = pa.schema([
    ("release_year", pa.int64()),
    ("measure_id", pa.int64()),
    ("measure_name", pa.string()),
    ("source_variable", pa.string()),
    ("has_raw_value", pa.bool_()),
    ("has_numerator", pa.bool_()),
    ("has_denominator", pa.bool_()),
    ("has_ci_low", pa.bool_()),
    ("has_ci_high", pa.bool_()),
])

_NULLISH = {"", ".", "na", "n/a", "*", "null", "none"}


def _to_float(s):
    if s is None:
        return None
    s = s.strip().replace(",", "")
    if s.lower() in _NULLISH:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _to_int(s):
    f = _to_float(s)
    return int(f) if f is not None else None


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content.decode("utf-8", errors="replace")


def _discover(pattern: str) -> dict:
    """Return {year:int -> absolute_url} for doc-page links matching pattern."""
    found = {}
    for page in DOC_PAGES:
        html = _fetch_text(page)
        for href in re.findall(r'href="([^"]+)"', html):
            m = re.search(pattern, href, re.I)
            if m and href.lower().endswith(".csv"):
                year = int(m.group(1))
                url = href if href.startswith("http") else HOST + href
                # later doc page wins ties harmlessly; one file per year either way
                found.setdefault(year, url)
                found[year] = url
    return found


def _flush(writer, schema, rows):
    if not rows:
        return
    cols = {f.name: [r.get(f.name) for r in rows] for f in schema}
    writer.write_table(pa.table(cols, schema=schema))
    rows.clear()


# ---------------------------------------------------------------------------
# trends
# ---------------------------------------------------------------------------

def fetch_trends(node_id: str) -> None:
    asset = node_id
    files = _discover(r"chr_trends_csv_(\d{4})")
    if not files:
        raise RuntimeError("no chr_trends_csv link discovered on documentation pages")
    # The trends file is cumulative; the latest release contains all history.
    url = files[max(files)]
    text = _fetch_text(url)

    reader = csv.reader(io.StringIO(text))
    header = [h.strip().lower() for h in next(reader)]
    idx = {name: i for i, name in enumerate(header)}
    required = ["yearspan", "measurename", "statecode", "countycode", "county",
                "state", "numerator", "denominator", "rawvalue", "cilow",
                "cihigh", "measureid"]
    missing = [c for c in required if c not in idx]
    if missing:
        raise RuntimeError(f"trends CSV missing expected columns: {missing}")

    def cell(row, name):
        i = idx.get(name)
        return row[i] if i is not None and i < len(row) else None

    rows = []
    n = 0
    with raw_parquet_writer(asset, TRENDS_SCHEMA) as writer:
        for row in reader:
            if not row:
                continue
            state_fips = (cell(row, "statecode") or "").strip().zfill(2)
            county_fips = (cell(row, "countycode") or "").strip().zfill(3)
            rows.append({
                "yearspan": (cell(row, "yearspan") or "").strip() or None,
                "measure_name": (cell(row, "measurename") or "").strip() or None,
                "measure_id": _to_int(cell(row, "measureid")),
                "state_fips": state_fips,
                "county_fips": county_fips,
                "fips": state_fips + county_fips,
                "county": (cell(row, "county") or "").strip() or None,
                "state": (cell(row, "state") or "").strip() or None,
                "numerator": _to_float(cell(row, "numerator")),
                "denominator": _to_float(cell(row, "denominator")),
                "raw_value": _to_float(cell(row, "rawvalue")),
                "ci_low": _to_float(cell(row, "cilow")),
                "ci_high": _to_float(cell(row, "cihigh")),
                "release_year": _to_int(cell(row, "chrreleaseyear")),
            })
            n += 1
            if len(rows) >= _BATCH_ROWS:
                _flush(writer, TRENDS_SCHEMA, rows)
        _flush(writer, TRENDS_SCHEMA, rows)
    print(f"  trends: wrote {n} rows from {url}")


# ---------------------------------------------------------------------------
# analytic
# ---------------------------------------------------------------------------

_ID_CODES = {"statecode", "countycode", "fipscode", "state", "county", "year"}
_STAT_RE = re.compile(r"^v(\d+)_(rawvalue|numerator|denominator|cilow|cihigh)$")


def _parse_analytic(text: str):
    """Yield uniform long rows from one wide analytic CSV (two-row header)."""
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if len(rows) < 3:
        raise RuntimeError("analytic CSV has fewer than 3 rows (expected 2 header rows + data)")
    names = rows[0]
    codes = [c.strip().lower() for c in rows[1]]
    if "statecode" not in codes:
        raise RuntimeError("analytic CSV second header row is not the variable-code row")

    idcol = {}
    measures = {}  # vid -> {stat: idx, "name": str}
    for i, code in enumerate(codes):
        if code in _ID_CODES:
            idcol[code] = i
        m = _STAT_RE.match(code)
        if m:
            vid = int(m.group(1))
            stat = m.group(2)
            d = measures.setdefault(vid, {})
            d[stat] = i
            if stat == "rawvalue":
                hn = names[i].strip()
                d["name"] = hn[: -len(" raw value")].strip() if hn.lower().endswith(" raw value") else hn

    for req in ("statecode", "countycode", "fipscode", "year"):
        if req not in idcol:
            raise RuntimeError(f"analytic CSV missing id column code '{req}'")
    if not measures:
        raise RuntimeError("analytic CSV exposed no v###_rawvalue measure columns")

    def g(row, i):
        return row[i] if i is not None and i < len(row) else None

    for row in rows[2:]:
        if not row:
            continue
        release_year = _to_int(g(row, idcol["year"]))
        state_fips = (g(row, idcol["statecode"]) or "").strip().zfill(2)
        county_fips = (g(row, idcol["countycode"]) or "").strip().zfill(3)
        fips = (g(row, idcol["fipscode"]) or "").strip().zfill(5)
        state = (g(row, idcol.get("state")) or "").strip() or None
        county = (g(row, idcol.get("county")) or "").strip() or None
        for vid, d in measures.items():
            raw_value = _to_float(g(row, d.get("rawvalue")))
            numerator = _to_float(g(row, d.get("numerator")))
            denominator = _to_float(g(row, d.get("denominator")))
            ci_low = _to_float(g(row, d.get("cilow")))
            ci_high = _to_float(g(row, d.get("cihigh")))
            if raw_value is None and numerator is None and denominator is None:
                continue
            yield {
                "release_year": release_year,
                "state_fips": state_fips,
                "county_fips": county_fips,
                "fips": fips,
                "state": state,
                "county": county,
                "measure_id": vid,
                "measure_name": d.get("name"),
                "raw_value": raw_value,
                "numerator": numerator,
                "denominator": denominator,
                "ci_low": ci_low,
                "ci_high": ci_high,
            }


def fetch_analytic(node_id: str) -> None:
    asset = node_id
    files = _discover(r"analytic_data(\d{4})")
    if len(files) < 8:
        raise RuntimeError(
            f"discovered only {len(files)} analytic files; expected the full "
            f"2010-present set (>=8). Documentation page layout may have changed."
        )

    rows = []
    total = 0
    with raw_parquet_writer(asset, ANALYTIC_SCHEMA) as writer:
        for year in sorted(files):
            text = _fetch_text(files[year])
            count = 0
            for rec in _parse_analytic(text):
                rows.append(rec)
                count += 1
                total += 1
                if len(rows) >= _BATCH_ROWS:
                    _flush(writer, ANALYTIC_SCHEMA, rows)
            _flush(writer, ANALYTIC_SCHEMA, rows)
            print(f"  analytic {year}: {count} long rows")
        if total == 0:
            raise RuntimeError("analytic produced 0 rows across all years")
    print(f"  analytic: wrote {total} rows across {len(files)} release years")


# ---------------------------------------------------------------------------
# measures
# ---------------------------------------------------------------------------

def fetch_measures(node_id: str) -> None:
    asset = node_id
    files = _discover(r"analytic_data(\d{4})")
    if not files:
        raise RuntimeError("no analytic_data link discovered on documentation pages")

    release_year = max(files)
    text = _fetch_text(files[release_year])
    reader = csv.reader(io.StringIO(text))
    names = next(reader)
    codes = [c.strip().lower() for c in next(reader)]

    measures = {}
    for i, code in enumerate(codes):
        m = _STAT_RE.match(code)
        if not m:
            continue
        vid = int(m.group(1))
        stat = m.group(2)
        rec = measures.setdefault(vid, {
            "release_year": release_year,
            "measure_id": vid,
            "measure_name": None,
            "source_variable": f"v{vid:03d}",
            "has_raw_value": False,
            "has_numerator": False,
            "has_denominator": False,
            "has_ci_low": False,
            "has_ci_high": False,
        })
        rec[f"has_{stat}"] = True
        if stat == "rawvalue":
            hn = names[i].strip()
            rec["measure_name"] = hn[: -len(" raw value")].strip() if hn.lower().endswith(" raw value") else hn

    rows = [measures[k] for k in sorted(measures)]
    if len(rows) < 50:
        raise RuntimeError(f"discovered only {len(rows)} measures in latest analytic file")
    with raw_parquet_writer(asset, MEASURES_SCHEMA) as writer:
        writer.write_table(pa.table({f.name: [r.get(f.name) for r in rows] for f in MEASURES_SCHEMA}, schema=MEASURES_SCHEMA))
    print(f"  measures: wrote {len(rows)} rows from analytic {release_year}")


# ---------------------------------------------------------------------------
# specs
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="county-health-rankings-trends", fn=fetch_trends, kind="download"),
    NodeSpec(id="county-health-rankings-analytic", fn=fetch_analytic, kind="download"),
    NodeSpec(id="county-health-rankings-measures", fn=fetch_measures, kind="download"),
]
