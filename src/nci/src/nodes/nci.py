"""NCI cancer statistics — SEER*Explorer + State Cancer Profiles.

Two NCI statistical surfaces, one node module (nine download nodes):

* SEER*Explorer (seer.cancer.gov) — NCI's national cancer-statistics engine.
  Its server-side `render_region_5.php` returns (double-encoded) JSON
  {info, data}: `info.key-order` names the dimensions encoded in each `data`
  key (e.g. "2_1_1_1_1_1"), `info.data-fields` names the positional columns of
  each `data_series` row. We fetch one statistic type per node, iterating every
  cancer site available for that statistic (discovered from
  `render_region_3_controls.php`), broken down by sex, and resolve dimension ids
  to labels via `get_var_formats.php`. `seer-explorer-cancer-sites` is the
  canonical site taxonomy (id -> label) joinable to every statistic table.

* State Cancer Profiles (statecancerprofiles.cancer.gov, NCI + CDC) —
  geographic incidence/mortality rates. `index.php?...&output=1` returns a CSV
  with title lines, one header row, state data rows (FIPS in column 2) and
  trailing footnotes; we parse the data rows, strip footnote markers like
  "Kentucky(7)" and bracketed header note tokens, and iterate every cancer type
  (discovered from the page's cancer dropdown) x sex at US/state level.

Stateless full re-pull for every node: the whole corpus is a few hundred small
JSON/CSV responses and refreshes annually with the new SEER/USCS submission, so
there is no incremental filter to exploit. Raw is written as NDJSON per node —
the column set is stable within a statistic but differs across statistics
(incidence carries year/rate, survival carries stage/percent, etc.), so a single
declared parquet schema does not fit; the model stage types each on read.
"""
import csv
import io
import json
import re

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

SEER_BASE = (
    "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"
)
SCP_BASE = "https://statecancerprofiles.cancer.gov/"


# ---- HTTP with honest retry classification -------------------------------


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    # SEER*Explorer endpoints return a JSON-encoded string (double-encoded).
    return json.loads(body) if isinstance(body, str) else body


@transient_retry()
def _get_text(url, **params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _seer_formats() -> dict:
    return _get_json(SEER_BASE + "get_var_formats.php")["VariableFormats"]


# ======================= SEER*Explorer cancer sites =======================


def fetch_seer_sites(node_id: str) -> None:
    """The canonical SEER*Explorer cancer-site taxonomy: id -> label plus the
    'active' flag from CancerSites. Reference data joinable to every statistic
    table via the site column."""
    asset = node_id
    payload = _get_json(SEER_BASE + "get_var_formats.php")
    site_labels = payload["VariableFormats"]["site"]  # {id: label}
    active = {
        str(d.get("value")): bool(d.get("active"))
        for d in (payload.get("CancerSites") or [])
        if isinstance(d, dict)
    }
    records = [
        {
            "site_id": int(sid),
            "site_label": label,
            "active": active.get(str(sid), False),
        }
        for sid, label in site_labels.items()
    ]
    if len(records) < 10:
        raise AssertionError(
            f"{asset}: only {len(records)} cancer sites — expected dozens"
        )
    save_raw_ndjson(records, asset)


# ====================== SEER*Explorer statistics ==========================

# slug (entity id minus the "seer-explorer-" prefix) -> fetch configuration.
# graph_type picks the view whose response carries the richest series for that
# statistic; `fixed` pins the non-series dimensions to their "all" value; `loop`
# fans an extra dimension that the view does NOT encode in its data key.
SEER_STATS = {
    "seer-incidence": {
        "data_type": 1,
        "graph_type": 1,  # Long-Term Trends -> rate by year
        "fixed": {"rate_type": 2, "race": 1, "age_range": 1, "subtype": 1},
        "loop": None,
    },
    "us-mortality": {
        "data_type": 2,
        "graph_type": 1,
        "fixed": {"race": 1, "age_range": 1},
        "loop": None,
    },
    "preliminary-incidence-rates": {
        "data_type": 3,
        "graph_type": 1,
        "fixed": {"rate_type": 2, "race": 1, "age_range": 1, "subtype": 1},
        "loop": None,
    },
    "survival": {
        "data_type": 4,
        "graph_type": 5,  # 5-Year Survival (relative survival %)
        "fixed": {"race": 1, "age_range": 1, "stage": 101},
        # survival's data key has no interval dim, so fan it explicitly:
        "loop": ("relative_survival_interval", [1, 2, 3, 5]),
    },
    "prevalence": {
        "data_type": 5,
        "graph_type": 1,
        "fixed": {"age_range": 1},
        "loop": None,
    },
    "risk-of-diagnosis-dying": {
        "data_type": 6,
        "graph_type": 1,
        "fixed": {"race": 1, "age_range": 300},
        "loop": ("stat_type", [10, 11]),  # 10=risk of diagnosis, 11=risk of dying
    },
}

# dimensions we resolve id -> human label from get_var_formats.php
_LABELLED_DIMS = (
    "site",
    "sex",
    "race",
    "age_range",
    "rate_type",
    "stage",
    "subtype",
    "stat_type",
    "relative_survival_interval",
)


def _seer_sites(data_type: int, graph_type: int) -> list:
    """The cancer sites available for a given statistic, per the source's own
    control endpoint. Raises if the shape changed (no silent under-coverage)."""
    ctrl = _get_json(
        SEER_BASE + "render_region_3_controls.php",
        site=1,
        data_type=data_type,
        graph_type=graph_type,
    )
    sites = ctrl["CheckboxValues"]["site"]["values"]
    if len(sites) < 10:
        raise AssertionError(
            f"data_type={data_type}: only {len(sites)} sites from controls "
            "endpoint — expected dozens; shape likely changed"
        )
    return [str(s) for s in sites]


def _flatten_seer(payload: dict, fmts: dict, slug: str, loop_field, loop_val) -> list:
    info = payload.get("info") or {}
    key_order = info.get("key-order") or []
    data_fields = info.get("data-fields") or []
    out = []
    for combo, series_obj in (payload.get("data") or {}).items():
        if not isinstance(series_obj, dict):
            continue
        series = series_obj.get("data_series")
        if not series:
            continue
        dims = dict(zip(key_order, combo.split("_")))
        base = {"statistic": slug}
        for dim, val in dims.items():
            base[dim] = val
            lm = fmts.get(dim)
            if dim in _LABELLED_DIMS and isinstance(lm, dict) and str(val) in lm:
                base[f"{dim}_label"] = lm[str(val)]
        if loop_field is not None:
            base[loop_field] = str(loop_val)
            lm = fmts.get(loop_field)
            if isinstance(lm, dict) and str(loop_val) in lm:
                base[f"{loop_field}_label"] = lm[str(loop_val)]
        for row in series:
            rec = dict(base)
            for field, value in zip(data_fields, row):
                rec[field] = value
            out.append(rec)
    return out


def fetch_seer_statistic(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len("nci-seer-explorer-"):]
    cfg = SEER_STATS[slug]
    fmts = _seer_formats()
    sites = _seer_sites(cfg["data_type"], cfg["graph_type"])

    loop_field, loop_vals = cfg["loop"] if cfg["loop"] else (None, [None])

    records = []
    for site in sites:
        for loop_val in loop_vals:
            params = {
                "site": site,
                "data_type": cfg["data_type"],
                "graph_type": cfg["graph_type"],
                "compareBy": "sex",
                "chk_sex_1": 1,
                "chk_sex_3": 1,
                "chk_sex_2": 1,
                "advopt_precision": 1,
                "advopt_show_ci": "on",
            }
            params.update(cfg["fixed"])
            if loop_field is not None:
                params[loop_field] = loop_val
            payload = _get_json(SEER_BASE + "render_region_5.php", **params)
            records.extend(
                _flatten_seer(payload, fmts, slug, loop_field, loop_val)
            )

    if not records:
        raise AssertionError(f"{asset}: fetched 0 records across {len(sites)} sites")
    save_raw_ndjson(records, asset)


# ========================= State Cancer Profiles ==========================

SCP_SEX = {"0": "Both Sexes", "1": "Male", "2": "Female"}


def _clean_header(cell: str) -> str:
    cell = re.sub(r"\(\[[^\]]*\]\)", "", cell)  # drop "([rate note])" tokens
    return cell.strip().strip('"').strip()


def _scp_cancers(path: str) -> list:
    """Discover (code, label) cancer types from the tool's own dropdown."""
    html = _get_text(SCP_BASE + path + "/")
    block = re.search(
        r"(?is)<select[^>]*name=[\"']?cancer[\"']?.*?</select>", html
    )
    if not block:
        raise AssertionError(f"SCP {path}: cancer <select> not found")
    opts = re.findall(
        r"<option[^>]*value=[\"']?(\d+)[\"']?[^>]*>(.*?)</option>",
        block.group(0),
    )
    cleaned = []
    for code, label in opts:
        text = re.sub(r"<[^>]+>", "", label)
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        cleaned.append((code, text.strip()))
    if len(cleaned) < 5:
        raise AssertionError(
            f"SCP {path}: parsed only {len(cleaned)} cancer options"
        )
    return cleaned


def _parse_scp_csv(txt: str) -> list:
    """Return the data rows of an SCP CSV as canonical dicts. Returns [] for an
    error/empty response (no 'State' header row) so the caller can skip the
    combination without failing the whole node."""
    rows = list(csv.reader(io.StringIO(txt)))
    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0].strip().strip('"') == "State":
            header_idx = i
            break
    if header_idx is None:
        return []
    headers = [_clean_header(c) for c in rows[header_idx]]
    low = [h.lower() for h in headers]
    try:
        i_rate = next(
            i
            for i in range(2, len(low))
            if "rate" in low[i] and "trend" not in low[i] and "rank" not in low[i]
        )
    except StopIteration:
        return []
    i_count = next((i for i in range(len(low)) if "count" in low[i]), None)
    i_dir = next((i for i in range(len(low)) if low[i] == "recent trend"), None)
    i_t5 = next((i for i in range(len(low)) if "5-year trend" in low[i]), None)

    out = []
    for row in rows[header_idx + 1:]:
        if len(row) <= i_rate + 2:
            continue
        if not re.match(r"^\d{5,6}$", row[1].strip()):
            continue  # only rows whose 2nd cell is a FIPS code are data
        area = re.sub(r"\(\d+\)", "", row[0]).strip().strip('"').strip()
        out.append(
            {
                "area": area,
                "fips": row[1].strip(),
                "rate": row[i_rate].strip(),
                "rate_lower_ci": row[i_rate + 1].strip(),
                "rate_upper_ci": row[i_rate + 2].strip(),
                "avg_annual_count": (
                    row[i_count].strip() if i_count is not None else None
                ),
                "recent_trend": (
                    row[i_dir].strip() if i_dir is not None else None
                ),
                "recent_5yr_trend_pct": (
                    row[i_t5].strip() if i_t5 is not None else None
                ),
            }
        )
    return out


def fetch_scp(node_id: str) -> None:
    asset = node_id  # "nci-scp-incidence" | "nci-scp-mortality"
    if node_id.endswith("incidence"):
        path, type_, extra = "incidencerates", "incd", {"stage": "999"}
    else:
        path, type_, extra = "deathrates", "death", {}

    cancers = _scp_cancers(path)
    records = []
    for code, label in cancers:
        for sex in ("0", "1", "2"):
            params = {
                "stateFIPS": "00",
                "areatype": "state",
                "cancer": code,
                "race": "00",
                "sex": sex,
                "age": "001",
                "year": "0",
                "type": type_,
                "sortVariableName": "rate",
                "sortOrder": "desc",
                "output": "1",
            }
            params.update(extra)
            txt = _get_text(SCP_BASE + path + "/index.php", **params)
            for rec in _parse_scp_csv(txt):
                rec["cancer_code"] = code
                rec["cancer_label"] = label
                rec["sex_code"] = sex
                rec["sex_label"] = SCP_SEX[sex]
                records.append(rec)

    if not records:
        raise AssertionError(f"{asset}: fetched 0 data rows")
    save_raw_ndjson(records, asset)


# ============================ DOWNLOAD_SPECS ==============================

DOWNLOAD_SPECS = [
    NodeSpec(id="nci-seer-explorer-cancer-sites", fn=fetch_seer_sites, kind="download"),
    NodeSpec(id="nci-seer-explorer-seer-incidence", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-us-mortality", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-preliminary-incidence-rates", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-survival", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-prevalence", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-risk-of-diagnosis-dying", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-scp-incidence", fn=fetch_scp, kind="download"),
    NodeSpec(id="nci-scp-mortality", fn=fetch_scp, kind="download"),
]
