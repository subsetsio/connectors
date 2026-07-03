"""Cedefop Skills Forecast connector.

The Cedefop Skills Forecast online tool (https://www.cedefop.europa.eu/en/tools/
skills-forecast) renders its charts client-side from a folder of static JSON
panel files. Each panel is a wide table: a few dimension columns
(country_l2 + sector/occupation/qualification/age/gender) plus one integer
column per year 2015..2035. There is no auth and no incremental query — the
files ARE the bulk export (the official spreadsheet download is request-form
gated). The corpus is small (low single-digit MB) and republished ~annually
under a new vintage folder (currently 'skills-2026'), so the correct shape is a
**stateless full re-pull**: every run re-discovers the current vintage and
re-fetches every panel.

The data-folder path and the panel file list are not hardcoded — they are
re-discovered each run from the tool page's drupalSettings + aggregated JS
bundles, so a new forecast vintage (which rotates the 'skills-2026' segment) is
picked up automatically. Despite the .json.gz extension the server returns plain
JSON (already decompressed), so we parse the response text directly.

Each fetch melts the wide year columns into long format and collapses the
source's structural redundancy (identical EU-27 aggregates shipped in an `-eu`
companion; unlabelled component+total stacks in the qualification panel) down to
one row per dimension-tuple x year before saving NDJSON; the SQL transform is
then a thin rename/cast that publishes one Delta table per indicator panel.
"""

import re

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)
from constants import SUBSETS

TOOL_URL = "https://www.cedefop.europa.eu/en/tools/skills-forecast"
HOST = "https://www.cedefop.europa.eu/"
YEAR_RE = re.compile(r"\d{4}")


def _slug(path: str) -> str:
    """Filename stem minus the vintage prefix, e.g.
    /skills-2026/country/skills2026-country-occupations.json.gz -> country-occupations."""
    fname = path.rsplit("/", 1)[-1].replace(".json.gz", "")
    return re.sub(r"^skills?-?20\d\d-?", "", fname).strip("-")


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # Files are named .json.gz but served as already-decompressed JSON.
    return resp.json()


def _discover():
    """Re-discover the live Skills Forecast surface.

    Returns (base_url, static_paths, templated_prefixes, iso_codes):
      base_url           — absolute URL of the vintage data folder root
      static_paths       — every '/skills-<vintage>/<group>/<file>.json.gz' path
      templated_prefixes — path prefixes concatenated with a country ISO in the JS
      iso_codes          — lowercase country ISO codes from the tool's country <select>
    """
    html = _get_text(TOOL_URL)
    folder = re.search(r'skillsForecastDataFolder"\s*:\s*"([^"]+)"', html).group(1)
    folder = folder.replace("\\/", "/")
    js_urls = [
        m.group(1).replace("&amp;", "&")
        for m in re.finditer(r'src="(/files/js/js_[^"]+)"', html)
    ]
    hay = "".join(_get_text(HOST + u) for u in js_urls)
    static = sorted(set(re.findall(r"/skills-20\d\d/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+\.json\.gz", hay)))
    templ = sorted(set(re.findall(r'(/skills-20\d\d/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+-)(?=")', hay)))
    templ = [t for t in templ if not any(p.startswith(t) for p in static)]
    iso = []
    for code, _name in re.findall(r'<option[^>]+value="([a-z]{2,4})"[^>]*>([^<]+)</option>', html):
        if code not in iso:
            iso.append(code)
    if not static:
        raise AssertionError("Skills Forecast discovery found no panel files — page/JS layout changed")
    return HOST + folder, static, templ, iso


def _melt(records):
    """Wide (dim cols + year cols) -> long (dim cols + year + value), dropping nulls."""
    for rec in records:
        dims = {k: v for k, v in rec.items() if not YEAR_RE.fullmatch(str(k))}
        for k, v in rec.items():
            if YEAR_RE.fullmatch(str(k)) and v is not None:
                yield {**dims, "year": int(k), "value": v}


def _collapse(rows):
    """Enforce one row per dimension-tuple×year — the raw contract this
    connector promises.

    Some Skills Forecast panels carry structural redundancy under *identical*
    dimension columns, with no label to tell the rows apart:

      * the occupation/sector country panels ship an `-eu` companion file that
        merely repeats the EU-27 aggregate already present in the main panel
        (byte-identical values), and
      * the labour-force-by-qualification panel stacks two components plus their
        additive total (component + component = total) for every
        (country, qualification, year).

    Neither redundant series is something we publish, so we keep the maximum
    value per dimension-tuple×year. For the identical EU duplicates that is a
    no-op; for the stacked qualification panel the total is — being the sum of
    two non-negative components — always the maximum, so this deterministically
    selects the total. Panels that are already unique pass through untouched.
    """
    best = {}
    for row in rows:
        key = tuple(sorted((k, v) for k, v in row.items() if k != "value"))
        if key not in best or row["value"] > best[key]["value"]:
            best[key] = row
    return list(best.values())


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity = node_id[len("cedefop-"):]
    base, static, templ, iso = _discover()

    rows = []
    matched = [p for p in static if _slug(p) == entity]
    if matched:
        # canonical static panel (orientation duplicates collapse to one file) +
        # any EU-aggregate companion (its rows append as a country value).
        rows.extend(_melt(_get_json(base + matched[0])))
        for eu in [p for p in static if _slug(p) == entity + "-eu"]:
            rows.extend(_melt(_get_json(base + eu)))
    else:
        # templated family: one self-describing file per country (lowercase ISO).
        prefix = next((t for t in templ if _slug(t.rstrip("-") + ".json.gz") == entity), None)
        if prefix is None:
            raise AssertionError(f"no source file resolves for entity '{entity}'")
        fetched = 0
        for code in iso:
            try:
                rows.extend(_melt(_get_json(base + prefix + code + ".json.gz")))
                fetched += 1
            except Exception as exc:  # one missing country must not lose the rest
                print(f"WARN {asset}: country '{code}' fetch failed: {type(exc).__name__}: {exc}")
        if fetched == 0:
            raise AssertionError(f"{asset}: no country files fetched for templated family")

    if not rows:
        raise AssertionError(f"{asset}: melted to 0 rows — upstream panel shape changed")
    rows = _collapse(rows)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cedefop-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in SUBSETS
]


def _transform_sql(download_id: str, dims, value_col: str) -> str:
    # Rename country_l2 -> country; keep the other dimensions verbatim.
    select_dims = []
    for d in dims:
        if d == "country_l2":
            select_dims.append('country_l2 AS country')
        else:
            select_dims.append(d)
    dim_sql = ",\n            ".join(select_dims)
    # Raw is already collapsed to one row per dimension-tuple×year in the fetch
    # (see _collapse), so this QUALIFY is a defensive no-op — kept to guarantee
    # the published key holds even if an upstream vintage changes shape.
    key_cols = ", ".join(dims)
    return f'''
        SELECT
            {dim_sql},
            CAST(year AS INTEGER)  AS year,
            CAST(value AS BIGINT)  AS {value_col}
        FROM "{download_id}"
        WHERE value IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY {key_cols}, year ORDER BY value DESC) = 1
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"cedefop-{eid.lower().replace('_', '-')}-transform",
        deps=[f"cedefop-{eid.lower().replace('_', '-')}"],
        sql=_transform_sql(
            f"cedefop-{eid.lower().replace('_', '-')}",
            cfg["dims"],
            cfg["value_col"],
        ),
        key=tuple("country" if d == "country_l2" else d for d in cfg["dims"]) + ("year",),
        temporal="year",
    )
    for eid, cfg in SUBSETS.items()
]
