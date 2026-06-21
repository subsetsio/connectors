"""NCI State Cancer Profiles (statecancerprofiles.cancer.gov, NCI + CDC).

Geographic incidence/mortality rates. `index.php?...&output=1` returns a CSV
with title lines, one header row, state data rows (FIPS in column 1) and
trailing footnotes; we parse the data rows, strip footnote markers like
"Kentucky(7)" and bracketed header note tokens, and iterate every cancer type
(discovered from the page's cancer dropdown) x sex at US/state level.

Raw is written as NDJSON per node. Each TRANSFORM_SPEC types its own statistic.
"""
import csv
import io
import re

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

SCP_BASE = "https://statecancerprofiles.cancer.gov/"

# ---- HTTP with honest retry classification -------------------------------


@transient_retry()
def _get_text(url, **params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


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
    NodeSpec(id="nci-scp-incidence", fn=fetch_scp, kind="download"),
    NodeSpec(id="nci-scp-mortality", fn=fetch_scp, kind="download"),
]


# ============================ TRANSFORM_SPECS =============================

_SCP_SQL = """
    SELECT
        area                                    AS state,
        fips,
        cancer_label                            AS cancer_site,
        cancer_code,
        sex_label                               AS sex,
        TRY_CAST(rate AS DOUBLE)                AS rate_per_100k,
        TRY_CAST(rate_lower_ci AS DOUBLE)       AS rate_lower_ci,
        TRY_CAST(rate_upper_ci AS DOUBLE)       AS rate_upper_ci,
        TRY_CAST(avg_annual_count AS BIGINT)    AS avg_annual_count,
        recent_trend,
        TRY_CAST(recent_5yr_trend_pct AS DOUBLE) AS recent_5yr_trend_pct
    FROM "{dep}"
    WHERE TRY_CAST(rate AS DOUBLE) IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nci-scp-incidence-transform",
        deps=["nci-scp-incidence"],
        sql=_SCP_SQL.format(dep="nci-scp-incidence"),
    ),
    SqlNodeSpec(
        id="nci-scp-mortality-transform",
        deps=["nci-scp-mortality"],
        sql=_SCP_SQL.format(dep="nci-scp-mortality"),
    ),
]
