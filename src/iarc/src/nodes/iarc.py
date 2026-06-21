"""IARC — Global Cancer Observatory (GCO) + CI5.

Seven published subsets, all stateless full re-pulls (the sources are fixed
released vintages — GLOBOCAN 2022, CI5 Vol. XII — so each run re-fetches the
whole corpus and overwrites; "refresh" means picking up the next vintage):

  GCO gateway REST API (https://gco.iarc.fr/gateway_prod/api/):
    - globocan_estimates    data/rate/{sex}/{type}/{pops}/{cancers}/   (modelled 2022 incidence & mortality)
    - tomorrow_projections  data/prediction/{sex}/{type}/{pops}/{cancers}/ (burden projections to 2050)
    - overtime_rates        overtime/v2/21 data/population/...          (observed registry time series)
    - globocan_cancers      meta/cancers/all/                          (cancer-site dictionary)
    - globocan_populations  meta/populations/all/                      (population/geography dictionary)
  CI5 bulk ZIPs (https://gco.iarc.who.int/media/ci5/data/vol12/Download/):
    - ci5_xii_summary       CI5-XII.zip   cases.csv (registry x sex x site x age)
    - ci5_xii_detailed      CI5-XIId.zip  per-registry files (sex x detailed-site x age, cases + person-years)

The GCO data/ endpoints accept underscore-joined population AND cancer code
lists, so each value table is just 6 requests (sex in {0,1,2} x type in {0,1});
the response rows already carry sex/type/year, so we only flatten nested fields.
No auth, no documented/observed rate limit; the PHP backend occasionally returns
an error string in the JSON 'error' array rather than an HTTP error, so we check
it. Raw is written as NDJSON throughout (nested/heterogeneous-friendly); the SQL
transforms are thin cast-and-type passes.
"""

import io
import zipfile

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

GLOBOCAN = "https://gco.iarc.fr/gateway_prod/api/globocan/v3/2022"
OVERTIME = "https://gco.iarc.fr/gateway_prod/api/overtime/v2/21"
CI5_SUMMARY_URL = "https://gco.iarc.who.int/media/ci5/data/vol12/Download/CI5-XII.zip"
CI5_DETAILED_URL = "https://gco.iarc.who.int/media/ci5/data/vol12/Download/CI5-XIId.zip"

SEXES = (0, 1, 2)
TYPES = (0, 1)  # 0 = incidence, 1 = mortality

# CI5 5-year age bands. Summary cases.csv columns N0_4..N85,N_unk; detailed/pop
# files use age-group indices 1..19. Index i (1-based) -> band[i-1].
AGE_BANDS = [
    "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
    "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79",
    "80-84", "85+", "unknown",
]


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #

@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get("error"):
        # The GCO PHP backend reports query errors inside the JSON body.
        raise RuntimeError(f"GCO API error for {url}: {data['error']}")
    return data


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _codes(meta, key: str) -> str:
    return "_".join(str(rec[key]) for rec in meta)


# --------------------------------------------------------------------------- #
# GLOBOCAN meta dictionaries
# --------------------------------------------------------------------------- #

def fetch_globocan_cancers(node_id: str) -> None:
    rows = _get_json(f"{GLOBOCAN}/meta/cancers/all/")
    save_raw_ndjson(rows, node_id)


def fetch_globocan_populations(node_id: str) -> None:
    rows = _get_json(f"{GLOBOCAN}/meta/populations/all/")
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# GLOBOCAN 2022 estimates (Cancer Today)
# --------------------------------------------------------------------------- #

def fetch_globocan_estimates(node_id: str) -> None:
    cancers = _codes(_get_json(f"{GLOBOCAN}/meta/cancers/all/"), "cancer")
    pops = _codes(_get_json(f"{GLOBOCAN}/meta/populations/all/"), "country_code")
    out = []
    for sex in SEXES:
        for typ in TYPES:
            payload = _get_json(f"{GLOBOCAN}/data/rate/{sex}/{typ}/{pops}/{cancers}/")
            for r in payload.get("dataset", []):
                ui = r.get("ui") or {}
                out.append({
                    "country_code": r.get("country_code"),
                    "cancer_code": r.get("cancer_code"),
                    "sex": r.get("sex", sex),
                    "type": r.get("type", typ),
                    "total": r.get("total"),
                    "total_pop": r.get("total_pop"),
                    "asr": r.get("asr"),
                    "crude_rate": r.get("crude_rate"),
                    "cum_risk_74": r.get("cum_risk_74"),
                    "ui_low": ui.get("low"),
                    "ui_high": ui.get("high"),
                })
    save_raw_ndjson(out, node_id)


# --------------------------------------------------------------------------- #
# Cancer Tomorrow projections (same gateway, prediction endpoint)
# --------------------------------------------------------------------------- #

def fetch_tomorrow_projections(node_id: str) -> None:
    cancers = _codes(_get_json(f"{GLOBOCAN}/meta/cancers/all/"), "cancer")
    pops = _codes(_get_json(f"{GLOBOCAN}/meta/populations/all/"), "country_code")
    out = []
    for sex in SEXES:
        for typ in TYPES:
            payload = _get_json(f"{GLOBOCAN}/data/prediction/{sex}/{typ}/{pops}/{cancers}/")
            for r in payload.get("dataset", []):
                out.append({
                    "country_code": r.get("id"),
                    "cancer_code": r.get("cancer"),
                    "sex": r.get("sex", sex),
                    "type": r.get("type", typ),
                    "year": r.get("year"),
                    "cases_pred": r.get("cases_pred"),
                    "cases_base": r.get("cases_base"),
                    "change": r.get("change"),
                    "percent": r.get("percent"),
                })
    save_raw_ndjson(out, node_id)


# --------------------------------------------------------------------------- #
# Cancer Over Time observed series
# --------------------------------------------------------------------------- #

def fetch_overtime_rates(node_id: str) -> None:
    cancers = _codes(_get_json(f"{OVERTIME}/meta/cancers/all/"), "cancer")
    pops = _codes(_get_json(f"{OVERTIME}/meta/populations/all/"), "country_code")
    out = []
    for sex in SEXES:
        for typ in TYPES:
            url = (
                f"{OVERTIME}/data/population/{sex}/{typ}/{pops}/{cancers}/"
                f"?year_start=1900&year_end=2030"
            )
            payload = _get_json(url)
            for r in payload.get("dataset", []):
                ages = r.get("ages") or {}
                popn = r.get("populations") or {}
                cases = sum(v for v in ages.values() if isinstance(v, (int, float)))
                person_years = sum(v for v in popn.values() if isinstance(v, (int, float)))
                out.append({
                    "country_code": r.get("country", r.get("id")),
                    "cancer_code": r.get("cancer"),
                    "sex": r.get("sex", sex),
                    "type": r.get("type", typ),
                    "year": r.get("year"),
                    "cases": cases,
                    "person_years": person_years,
                })
    save_raw_ndjson(out, node_id)


# --------------------------------------------------------------------------- #
# CI5 Volume XII bulk downloads
# --------------------------------------------------------------------------- #

def _ci5_registry_labels(text: str) -> dict:
    """Registry.txt / registry_detailed.txt: '<code> [*] <label> <period>'."""
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        code, rest = parts
        if not code.isdigit():
            continue
        label = rest.lstrip("* ").strip()
        out[int(code)] = label
    return out


def fetch_ci5_xii_summary(node_id: str) -> None:
    import csv

    zf = zipfile.ZipFile(io.BytesIO(_get_bytes(CI5_SUMMARY_URL)))

    # cancer dictionary: "CANCER\tICD-10\tLABEL" with a header row
    cancer_label, cancer_icd = {}, {}
    cdict = zf.read("cancer_summary.txt").decode("utf-8", "replace").splitlines()
    for line in cdict[1:]:
        cols = [c.strip() for c in line.split("\t")]
        if len(cols) >= 3 and cols[0].isdigit():
            cancer_label[int(cols[0])] = cols[2]
            cancer_icd[int(cols[0])] = cols[1]

    registry_label = _ci5_registry_labels(zf.read("Registry.txt").decode("utf-8", "replace"))

    reader = csv.reader(io.StringIO(zf.read("cases.csv").decode("utf-8", "replace")))
    header = next(reader)
    # header: REGISTRY,SEX,CANCER,TOTAL,N0_4,...,N85,N_unk
    age_cols = header[4:]  # 19 age columns, aligned with AGE_BANDS order
    out = []
    for row in reader:
        if len(row) < 4:
            continue
        reg = int(row[0])
        sex = int(row[1])
        can = int(row[2])
        for i, raw in enumerate(row[4:]):
            band = AGE_BANDS[i] if i < len(AGE_BANDS) else f"col{i}"
            out.append({
                "registry_code": reg,
                "registry": registry_label.get(reg),
                "sex": sex,
                "cancer_code": can,
                "cancer": cancer_label.get(can),
                "icd10": cancer_icd.get(can),
                "age_band": band,
                "cases": int(raw) if raw not in ("", None) else 0,
            })
    save_raw_ndjson(out, node_id)


def fetch_ci5_xii_detailed(node_id: str) -> None:
    import csv

    zf = zipfile.ZipFile(io.BytesIO(_get_bytes(CI5_DETAILED_URL)))

    # cancer_detailed.txt: "001 All sites (...)" — fixed-width-ish: code then label
    cancer_label = {}
    for line in zf.read("cancer_detailed.txt").decode("utf-8", "replace").splitlines():
        line = line.rstrip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[0].isdigit():
            cancer_label[int(parts[0])] = parts[1].strip()

    registry_label = _ci5_registry_labels(
        zf.read("registry_detailed.txt").decode("utf-8", "replace")
    )

    out = []
    for name in zf.namelist():
        if not name.endswith(".csv"):
            continue
        reg = int(name[:-4]) if name[:-4].isdigit() else None
        if reg is None:
            continue
        reader = csv.reader(io.StringIO(zf.read(name).decode("utf-8", "replace")))
        for row in reader:
            if len(row) < 5:
                continue
            sex = int(row[0])
            site = int(row[1])
            age_idx = int(row[2])  # 1..19
            band = AGE_BANDS[age_idx - 1] if 1 <= age_idx <= len(AGE_BANDS) else f"idx{age_idx}"
            out.append({
                "registry_code": reg,
                "registry": registry_label.get(reg),
                "sex": sex,
                "cancer_code": site,
                "cancer": cancer_label.get(site),
                "age_band": band,
                "cases": int(row[3]) if row[3] not in ("", None) else 0,
                "person_years": int(row[4]) if row[4] not in ("", None) else 0,
            })
    save_raw_ndjson(out, node_id)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #

DOWNLOAD_SPECS = [
    NodeSpec(id="iarc-globocan-estimates", fn=fetch_globocan_estimates, kind="download"),
    NodeSpec(id="iarc-globocan-cancers", fn=fetch_globocan_cancers, kind="download"),
    NodeSpec(id="iarc-globocan-populations", fn=fetch_globocan_populations, kind="download"),
    NodeSpec(id="iarc-tomorrow-projections", fn=fetch_tomorrow_projections, kind="download"),
    NodeSpec(id="iarc-overtime-rates", fn=fetch_overtime_rates, kind="download"),
    NodeSpec(id="iarc-ci5-xii-summary", fn=fetch_ci5_xii_summary, kind="download"),
    NodeSpec(id="iarc-ci5-xii-detailed", fn=fetch_ci5_xii_detailed, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="iarc-globocan-estimates-transform",
        deps=["iarc-globocan-estimates"],
        sql='''
            SELECT
                CAST(country_code AS BIGINT)  AS country_code,
                CAST(cancer_code  AS BIGINT)  AS cancer_code,
                CAST(sex          AS INTEGER) AS sex,
                CAST(type         AS INTEGER) AS measure_type,
                CASE WHEN CAST(type AS INTEGER) = 0 THEN 'incidence' ELSE 'mortality' END AS measure,
                CAST(total        AS BIGINT)  AS cases,
                CAST(total_pop    AS BIGINT)  AS population,
                CAST(asr          AS DOUBLE)  AS asr,
                CAST(crude_rate   AS DOUBLE)  AS crude_rate,
                CAST(cum_risk_74  AS DOUBLE)  AS cum_risk_74,
                CAST(ui_low       AS BIGINT)  AS ui_low,
                CAST(ui_high      AS BIGINT)  AS ui_high
            FROM "iarc-globocan-estimates"
            WHERE total IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iarc-globocan-cancers-transform",
        deps=["iarc-globocan-cancers"],
        sql='''
            SELECT
                CAST(cancer AS BIGINT)        AS cancer_code,
                CAST(label AS VARCHAR)        AS label,
                CAST(short_label AS VARCHAR)  AS short_label,
                CAST(ICD AS VARCHAR)          AS icd10,
                CAST(gender AS INTEGER)       AS gender,
                CAST(cancer_order AS INTEGER) AS cancer_order
            FROM "iarc-globocan-cancers"
            WHERE cancer IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iarc-globocan-populations-transform",
        deps=["iarc-globocan-populations"],
        sql='''
            SELECT
                CAST(country_code AS BIGINT)  AS country_code,
                CAST(label AS VARCHAR)        AS label,
                CAST(country_iso3 AS VARCHAR) AS iso3,
                CAST(continent_code AS VARCHAR) AS continent_code,
                CAST(area_label AS VARCHAR)   AS area_label,
                CAST(grouping AS VARCHAR)     AS grouping,
                TRY_CAST(hdi_value AS DOUBLE) AS hdi_value,
                CAST(hdi_label AS VARCHAR)    AS hdi_label,
                CAST(income_label AS VARCHAR) AS income_label,
                CAST(who_region AS VARCHAR)   AS who_region,
                CAST(who_label AS VARCHAR)    AS who_label
            FROM "iarc-globocan-populations"
            WHERE country_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iarc-tomorrow-projections-transform",
        deps=["iarc-tomorrow-projections"],
        sql='''
            SELECT
                CAST(country_code AS BIGINT)  AS country_code,
                CAST(cancer_code  AS BIGINT)  AS cancer_code,
                CAST(sex          AS INTEGER) AS sex,
                CAST(type         AS INTEGER) AS measure_type,
                CASE WHEN CAST(type AS INTEGER) = 0 THEN 'incidence' ELSE 'mortality' END AS measure,
                CAST(year         AS INTEGER) AS year,
                CAST(cases_pred   AS DOUBLE)  AS cases_predicted,
                CAST(cases_base   AS DOUBLE)  AS cases_baseline,
                CAST(change       AS DOUBLE)  AS change,
                CAST(percent      AS DOUBLE)  AS percent_change
            FROM "iarc-tomorrow-projections"
            WHERE year IS NOT NULL AND cases_pred IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iarc-overtime-rates-transform",
        deps=["iarc-overtime-rates"],
        sql='''
            SELECT
                CAST(country_code AS BIGINT)  AS country_code,
                CAST(cancer_code  AS BIGINT)  AS cancer_code,
                CAST(sex          AS INTEGER) AS sex,
                CAST(type         AS INTEGER) AS measure_type,
                CASE WHEN CAST(type AS INTEGER) = 0 THEN 'incidence' ELSE 'mortality' END AS measure,
                CAST(year         AS INTEGER) AS year,
                CAST(cases        AS BIGINT)  AS cases,
                CAST(person_years AS BIGINT)  AS person_years,
                CASE WHEN CAST(person_years AS DOUBLE) > 0
                     THEN CAST(cases AS DOUBLE) / CAST(person_years AS DOUBLE) * 100000
                END                           AS crude_rate_per_100k
            FROM "iarc-overtime-rates"
            WHERE year IS NOT NULL AND person_years > 0
        ''',
    ),
    SqlNodeSpec(
        id="iarc-ci5-xii-summary-transform",
        deps=["iarc-ci5-xii-summary"],
        sql='''
            SELECT
                CAST(registry_code AS BIGINT) AS registry_code,
                CAST(registry AS VARCHAR)     AS registry,
                CAST(sex AS INTEGER)          AS sex,
                CAST(cancer_code AS BIGINT)   AS cancer_code,
                CAST(cancer AS VARCHAR)       AS cancer,
                CAST(icd10 AS VARCHAR)        AS icd10,
                CAST(age_band AS VARCHAR)     AS age_band,
                CAST(cases AS BIGINT)         AS cases
            FROM "iarc-ci5-xii-summary"
            WHERE registry_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iarc-ci5-xii-detailed-transform",
        deps=["iarc-ci5-xii-detailed"],
        sql='''
            SELECT
                CAST(registry_code AS BIGINT) AS registry_code,
                CAST(registry AS VARCHAR)     AS registry,
                CAST(sex AS INTEGER)          AS sex,
                CAST(cancer_code AS BIGINT)   AS cancer_code,
                CAST(cancer AS VARCHAR)       AS cancer,
                CAST(age_band AS VARCHAR)     AS age_band,
                CAST(cases AS BIGINT)         AS cases,
                CAST(person_years AS BIGINT)  AS person_years
            FROM "iarc-ci5-xii-detailed"
            WHERE registry_code IS NOT NULL
        ''',
    ),
]
