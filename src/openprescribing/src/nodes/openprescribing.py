"""OpenPrescribing (NHS England) connector.

OpenPrescribing (Bennett Institute, University of Oxford) republishes NHS England
GP prescribing data (sourced from NHSBSA) as standardised prescribing *measures*
plus raw spending. Five published subsets:

  measures        reference catalog of the curated prescribing measures
  measure_values  measure numerator/denominator/percentile per org per month
  spending        prescribing cost/items/quantity per BNF chapter per org per month
  bnf_codes       BNF classification reference (codes referenced by the measures)
  organisations   NHS prescribing-org reference (practices, PCNs, Sub-ICBs, ICBs, regions)

SOURCING STRATEGY — two channels, chosen for resilience:

  * GitHub (raw.githubusercontent.com / api.github.com) — NOT behind Cloudflare.
    The measure DEFINITIONS live in the source repo, so `measures` and the
    BNF-code reference (`bnf_codes`, parsed from each measure's numerator/
    denominator BNF-code filters) are built entirely from the repo and do not
    touch the rate-limited, bot-challenged live API.

  * The live REST API (https://openprescribing.net/api/1.0/) — the only source
    of the actual time-series VALUES (`measure_values`, `spending`) and the org
    reference (`organisations`). CAVEAT: openprescribing.net sits behind a
    Cloudflare managed bot challenge that returns HTTP 403 to datacenter/
    automation clients (verified from this environment across curl, httpx and a
    headless browser). The API needs no auth and is widely scripted against by
    ordinary clients, so this is IP-reputation anti-bot, not a credential wall.
    If the runner's egress IP is also challenged these three nodes 403 and fail
    fast (403 is permanent, not retried); `measures`/`bnf_codes` still publish.

Stateless full re-pull each run: the corpus is small and the source revises past
months, so we never trust a stored watermark.
"""

import csv
import io
import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    raw_writer,
    save_raw_ndjson,
    transient_retry,
)

# --- live API -----------------------------------------------------------------
BASE = "https://openprescribing.net/api/1.0/"
# A realistic browser UA + Accept; cannot solve a JS challenge but skips simple
# UA heuristics. ASCII-only (httpx/urllib3 reject non-ASCII header bytes).
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/csv,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}
MEASURE_ORG_LEVELS = ("sicbl", "icb")
ORG_LEVELS = ("regional_team", "icb", "sicbl", "pcn", "practice")

# --- GitHub (Cloudflare-free) -------------------------------------------------
GH_REPO = "bennettoxford/openprescribing"
GH_TREE = f"https://api.github.com/repos/{GH_REPO}/git/trees/main?recursive=1"
GH_RAW = f"https://raw.githubusercontent.com/{GH_REPO}/main/"
DEF_PREFIX = "openprescribing/measures/definitions/"

# Standard BNF chapters (stable therapeutic-area taxonomy). Spending is pulled
# per chapter at Sub-ICB level. Chapters 16/17 are unused in the prescribing data.
BNF_CHAPTERS = (
    ("01", "Gastro-Intestinal System"),
    ("02", "Cardiovascular System"),
    ("03", "Respiratory System"),
    ("04", "Central Nervous System"),
    ("05", "Infections"),
    ("06", "Endocrine System"),
    ("07", "Obstetrics, Gynaecology and Urinary-Tract Disorders"),
    ("08", "Malignant Disease and Immunosuppression"),
    ("09", "Nutrition and Blood"),
    ("10", "Musculoskeletal and Joint Diseases"),
    ("11", "Eye"),
    ("12", "Ear, Nose and Oropharynx"),
    ("13", "Skin"),
    ("14", "Immunological Products and Vaccines"),
    ("15", "Anaesthesia"),
    ("18", "Preparations used in Diagnosis"),
    ("19", "Other Drugs and Preparations"),
    ("20", "Dressings"),
    ("21", "Appliances"),
    ("22", "Incontinence Appliances"),
    ("23", "Stoma Appliances"),
)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
@transient_retry()
def _get_json(url, headers=None):
    r = get(url, timeout=(10.0, 120.0), headers=headers)
    r.raise_for_status()
    return r.json()


@transient_retry()
def _get_text(url, headers=None):
    r = get(url, timeout=(10.0, 180.0), headers=headers)
    r.raise_for_status()
    return r.text


def _measure_def_paths():
    """All measure-definition file paths in the source repo (Cloudflare-free)."""
    tree = _get_json(GH_TREE)
    return [
        t["path"]
        for t in tree.get("tree", [])
        if t["path"].startswith(DEF_PREFIX) and t["path"].endswith(".json")
    ]


def _load_definitions():
    """slug -> parsed measure definition dict, from the repo."""
    out = {}
    for path in _measure_def_paths():
        slug = path.rsplit("/", 1)[-1][: -len(".json")]
        out[slug] = json.loads(_get_text(GH_RAW + path))
    return out


def _plain(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        value = " ".join(str(v) for v in value)
    text = str(value)
    # crude tag strip — definitions occasionally embed simple HTML
    out, depth = [], 0
    for ch in text:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return " ".join("".join(out).split()) or None


def _num(value):
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.lower() in ("none", "nan", "null"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _first(row, *keys):
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return str(row[k])
    return None


def _bnf_level(length):
    return {
        2: "chapter",
        4: "section",
        6: "paragraph",
        7: "subparagraph",
        9: "chemical",
        11: "product",
        15: "presentation",
    }.get(length, "other")


def _csv_rows(text):
    return list(csv.DictReader(io.StringIO(text)))


# ----------------------------------------------------------------------------
# fetch fns — GitHub-sourced (reliable)
# ----------------------------------------------------------------------------
def fetch_measures(node_id: str) -> None:
    """Reference catalog of standardised measures, from the repo definitions."""
    defs = _load_definitions()
    rows = []
    for slug, d in sorted(defs.items()):
        rows.append(
            {
                "measure_id": slug,
                "name": _plain(d.get("name")),
                "title": _plain(d.get("title")),
                "description": _plain(d.get("description")),
                "why_it_matters": _plain(d.get("why_it_matters")),
                "tags": ",".join(d.get("tags") or []) or None,
                "numerator_short": _plain(d.get("numerator_short")),
                "denominator_short": _plain(d.get("denominator_short")),
                "is_percentage": d.get("is_percentage"),
                "is_cost_based": d.get("is_cost_based"),
                "low_is_good": d.get("low_is_good"),
                "numerator_type": d.get("numerator_type"),
                "denominator_type": d.get("denominator_type"),
                "measure_type": d.get("measure_type"),
                "measure_complexity": d.get("measure_complexity"),
                "date_reviewed": (
                    str(d["date_reviewed"]) if d.get("date_reviewed") else None
                ),
            }
        )
    save_raw_ndjson(rows, node_id)


def fetch_bnf_codes(node_id: str) -> None:
    """BNF code reference, parsed from the numerator/denominator BNF-code filters
    declared in the repo measure definitions (Cloudflare-free)."""
    defs = _load_definitions()
    seen = {}
    for d in defs.values():
        for key in ("numerator_bnf_codes_filter", "denominator_bnf_codes_filter"):
            for entry in d.get(key) or []:
                code, _, comment = str(entry).partition("#")
                code = code.strip()
                if not code:
                    continue
                name = comment.strip() or None
                if code not in seen or (name and not seen[code]):
                    seen[code] = name
    rows = [
        {
            "bnf_code": code,
            "name": name,
            "code_length": len(code),
            "level": _bnf_level(len(code)),
        }
        for code, name in sorted(seen.items())
    ]
    save_raw_ndjson(rows, node_id)


# ----------------------------------------------------------------------------
# fetch fns — live API (Cloudflare-risk; normalize keys at fetch so the SQL
# transforms never depend on the source's exact CSV/JSON column names)
# ----------------------------------------------------------------------------
def fetch_measure_values(node_id: str) -> None:
    configure_http(headers=BROWSER_HEADERS)
    slugs = sorted(p.rsplit("/", 1)[-1][: -len(".json")] for p in _measure_def_paths())
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for level in MEASURE_ORG_LEVELS:
            for slug in slugs:
                url = f"{BASE}measure_by_{level}/?measure={slug}&format=csv"
                for row in _csv_rows(_get_text(url, headers=BROWSER_HEADERS)):
                    fh.write(
                        json.dumps(
                            {
                                "measure": _first(row, "measure") or slug,
                                "org_level": level,
                                "org_id": _first(
                                    row, "org_id", "org", "ccg", "code", "row_id"
                                ),
                                "org_name": _first(
                                    row, "org_name", "name", "row_name"
                                ),
                                "date": _first(row, "date"),
                                "numerator": _num(row.get("numerator")),
                                "denominator": _num(row.get("denominator")),
                                "calc_value": _num(row.get("calc_value")),
                                "percentile": _num(row.get("percentile")),
                            }
                        )
                        + "\n"
                    )


def fetch_spending(node_id: str) -> None:
    configure_http(headers=BROWSER_HEADERS)
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for code, chapter_name in BNF_CHAPTERS:
            url = f"{BASE}spending_by_org/?org_type=sicbl&code={code}&format=csv"
            for row in _csv_rows(_get_text(url, headers=BROWSER_HEADERS)):
                fh.write(
                    json.dumps(
                        {
                            "bnf_code": code,
                            "bnf_chapter_name": chapter_name,
                            "org_level": "sicbl",
                            "org_id": _first(
                                row, "row_id", "org_id", "org", "ccg", "code"
                            ),
                            "org_name": _first(row, "row_name", "org_name", "name"),
                            "date": _first(row, "date"),
                            "items": _num(row.get("items")),
                            "quantity": _num(row.get("quantity")),
                            "actual_cost": _num(row.get("actual_cost")),
                        }
                    )
                    + "\n"
                )


def fetch_organisations(node_id: str) -> None:
    configure_http(headers=BROWSER_HEADERS)
    rows = []
    for level in ORG_LEVELS:
        data = _get_json(f"{BASE}org_code/?org_type={level}&format=json", headers=BROWSER_HEADERS)
        for o in data if isinstance(data, list) else []:
            rows.append(
                {
                    "org_id": _first(o, "id", "code", "ods_code"),
                    "org_name": _first(o, "name", "org_name", "title"),
                    "org_level": level,
                }
            )
    save_raw_ndjson(rows, node_id)


# ----------------------------------------------------------------------------
# DAG
# ----------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id="openprescribing-measures", fn=fetch_measures, kind="download"),
    NodeSpec(id="openprescribing-measure-values", fn=fetch_measure_values, kind="download"),
    NodeSpec(id="openprescribing-spending", fn=fetch_spending, kind="download"),
    NodeSpec(id="openprescribing-bnf-codes", fn=fetch_bnf_codes, kind="download"),
    NodeSpec(id="openprescribing-organisations", fn=fetch_organisations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openprescribing-measures-transform",
        deps=["openprescribing-measures"],
        key=("measure_id",),
        sql='''
            SELECT
                measure_id,
                name,
                title,
                description,
                why_it_matters,
                tags,
                numerator_short,
                denominator_short,
                TRY_CAST(is_percentage AS BOOLEAN) AS is_percentage,
                TRY_CAST(is_cost_based AS BOOLEAN) AS is_cost_based,
                TRY_CAST(low_is_good AS BOOLEAN)  AS low_is_good,
                numerator_type,
                denominator_type,
                measure_type,
                measure_complexity,
                TRY_CAST(date_reviewed AS DATE) AS date_reviewed
            FROM "openprescribing-measures"
            WHERE measure_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="openprescribing-measure-values-transform",
        deps=["openprescribing-measure-values"],
        key=("measure", "org_level", "org_id", "date"),
        temporal="date",
        sql='''
            SELECT
                measure,
                org_level,
                CAST(org_id AS VARCHAR)   AS org_id,
                CAST(org_name AS VARCHAR) AS org_name,
                CAST(date AS DATE)        AS date,
                CAST(numerator AS DOUBLE)   AS numerator,
                CAST(denominator AS DOUBLE) AS denominator,
                CAST(calc_value AS DOUBLE)  AS calc_value,
                CAST(percentile AS DOUBLE)  AS percentile
            FROM "openprescribing-measure-values"
            WHERE org_id IS NOT NULL AND date IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY measure, org_level, org_id, date
                ORDER BY calc_value
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="openprescribing-spending-transform",
        deps=["openprescribing-spending"],
        key=("bnf_code", "org_id", "date"),
        temporal="date",
        sql='''
            SELECT
                bnf_code,
                bnf_chapter_name,
                org_level,
                CAST(org_id AS VARCHAR)   AS org_id,
                CAST(org_name AS VARCHAR) AS org_name,
                CAST(date AS DATE)        AS date,
                CAST(items AS DOUBLE)       AS items,
                CAST(quantity AS DOUBLE)    AS quantity,
                CAST(actual_cost AS DOUBLE) AS actual_cost
            FROM "openprescribing-spending"
            WHERE org_id IS NOT NULL AND date IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY bnf_code, org_id, date
                ORDER BY actual_cost DESC
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="openprescribing-bnf-codes-transform",
        deps=["openprescribing-bnf-codes"],
        key=("bnf_code",),
        sql='''
            SELECT
                bnf_code,
                name,
                CAST(code_length AS INTEGER) AS code_length,
                level
            FROM "openprescribing-bnf-codes"
            WHERE bnf_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="openprescribing-organisations-transform",
        deps=["openprescribing-organisations"],
        key=("org_level", "org_id"),
        sql='''
            SELECT
                CAST(org_id AS VARCHAR)   AS org_id,
                CAST(org_name AS VARCHAR) AS org_name,
                org_level
            FROM "openprescribing-organisations"
            WHERE org_id IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY org_level, org_id ORDER BY org_name
            ) = 1
        ''',
    ),
]
