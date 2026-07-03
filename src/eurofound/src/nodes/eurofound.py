"""Eurofound connector — the two named statistical databases Eurofound publishes
as bulk files on its non-checkpoint CDNs (the public "data catalogue" itself is
locked behind a Vercel bot challenge and exposes only chart images, so it is not
machine-fetchable; see research/collect notes).

Subsets published:
  - collectively-agreed-wages-rates       (xlsx "Rates" sheet, ~198k obs)
  - collectively-agreed-wages-agreements  (xlsx "CollectiveAgreements" sheet)
  - covid19-eu-policywatch                (covid19db.json, ~3167 measures)

Both source files are full snapshots fetched in one request — stateless full
re-pull every refresh (a few MB, no incremental filter exists).
"""

import io

import openpyxl
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

# Stable CDN URLs verified during research (NOT behind the www checkpoint).
MW_XLSX_URL = "https://a.storyblok.com/f/279033/x/5d93553ab8/2025update_ca_mwdatabase_downloaddataset.xlsx"
COVID_JSON_URL = "https://static.eurofound.europa.eu/covid19db/data/covid19db.json"

# Curated column renames (source header -> clean snake_case). Only mapped
# columns are kept in the raw asset.
RATES_MAP = {
    "CountryName": "country",
    "c_date - Year": "year",
    "c_date - Month": "month",
    "c_originalSector": "sector",
    "c_type_new": "wage_type",
    "frequency": "frequency",
    "currency": "currency",
    "value": "value",
    "workingHours": "working_hours",
    "numberAnnualPayments": "annual_payments",
    "c_ColAgr_Series": "series",
    "SeriesTitle": "series_title",
    "c_identifier_pbi": "agreement_id",
    "rateSMW_eur_month": "rate_eur_month",
    "rateSMW_nat_month": "rate_nat_month",
    "rateSMW_eur_hrs": "rate_eur_hour",
    "rateSMW_nat_hrs": "rate_nat_hour",
    "rateTransformedEuro": "rate_eur",
    "rateTransformed": "rate_national",
}

AGREEMENTS_MAP = {
    "c_identifier_pbi": "agreement_id",
    "CountryName": "country",
    "titleEnglish": "title_en",
    "titleNative": "title_native",
    "bargainingLevel": "bargaining_level",
    "c_originalSector": "sector",
    "PanelOfObservations": "in_panel",
}

COVID_MAP = {
    "title": "title",
    "d_startDate": "start_date",
    "d_endDate": "end_date",
    "calc_country": "country",
    "calc_minorCategory": "category",
    "calc_subMinorCategory": "subcategory",
    "calc_identifier": "identifier",
    "calc_type": "measure_type",
    "statusOfRegulation": "status",
    "dateType": "date_type",
    "calc_creationDay": "creation_day",
    "calc_lastUpdate": "last_update",
    "isSector": "is_sector",
    "isOccupation": "is_occupation",
    "sector_privateOrPublic": "sector_scope",
    "socialPartner_role": "social_partner_role",
}


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _read_sheet(content: bytes, sheet: str, colmap: dict) -> list[dict]:
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    try:
        ws = wb[sheet]
        it = ws.iter_rows(values_only=True)
        header = list(next(it))
        idx = {h: i for i, h in enumerate(header)}
        missing = [src for src in colmap if src not in idx]
        if missing:
            raise AssertionError(f"sheet '{sheet}' missing expected columns: {missing}")
        rows = []
        for r in it:
            if r is None or all(v is None for v in r):
                continue
            rows.append({dst: r[idx[src]] for src, dst in colmap.items()})
        return rows
    finally:
        wb.close()


def fetch_mw_rates(node_id: str) -> None:
    rows = _read_sheet(_get_bytes(MW_XLSX_URL), "Rates", RATES_MAP)
    save_raw_ndjson(rows, node_id)


def fetch_mw_agreements(node_id: str) -> None:
    rows = _read_sheet(_get_bytes(MW_XLSX_URL), "CollectiveAgreements", AGREEMENTS_MAP)
    save_raw_ndjson(rows, node_id)


def fetch_covid_policywatch(node_id: str) -> None:
    data = _get_json(COVID_JSON_URL)
    rows = []
    for rec in data:
        fd = rec.get("fieldData", {}) or {}
        row = {dst: fd.get(src) for src, dst in COVID_MAP.items()}
        row["record_id"] = rec.get("recordId")
        rows.append(row)
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="eurofound-collectively-agreed-wages-rates", fn=fetch_mw_rates, kind="download"),
    NodeSpec(id="eurofound-collectively-agreed-wages-agreements", fn=fetch_mw_agreements, kind="download"),
    NodeSpec(id="eurofound-covid19-eu-policywatch", fn=fetch_covid_policywatch, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="eurofound-collectively-agreed-wages-rates-transform",
        deps=["eurofound-collectively-agreed-wages-rates"],
        temporal="period",
        sql='''
            SELECT
                country,
                CAST(year AS INTEGER)                                       AS year,
                month,
                CAST(try_strptime(NULLIF(month, '') || ' ' || CAST(year AS VARCHAR), '%B %Y') AS DATE) AS period,
                sector,
                wage_type,
                frequency,
                series,
                series_title,
                agreement_id,
                TRY_CAST(value AS DOUBLE)            AS value,
                TRY_CAST(rate_eur AS DOUBLE)         AS rate_eur,
                TRY_CAST(rate_national AS DOUBLE)    AS rate_national,
                TRY_CAST(rate_eur_month AS DOUBLE)   AS rate_eur_month,
                TRY_CAST(rate_nat_month AS DOUBLE)   AS rate_nat_month,
                TRY_CAST(working_hours AS DOUBLE)    AS working_hours,
                TRY_CAST(annual_payments AS DOUBLE)  AS annual_payments
            FROM "eurofound-collectively-agreed-wages-rates"
            WHERE country IS NOT NULL AND year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="eurofound-collectively-agreed-wages-agreements-transform",
        deps=["eurofound-collectively-agreed-wages-agreements"],
        key=("agreement_id",),
        sql='''
            SELECT
                agreement_id,
                country,
                title_en,
                title_native,
                bargaining_level,
                sector,
                TRY_CAST(in_panel AS INTEGER) AS in_panel
            FROM "eurofound-collectively-agreed-wages-agreements"
            -- real agreement ids look like 'CA-AT-1865'; this also drops the
            -- trailing "Applied filters: ..." footer note row in the xlsx sheet.
            WHERE agreement_id LIKE 'CA-%'
        ''',
    ),
    SqlNodeSpec(
        id="eurofound-covid19-eu-policywatch-transform",
        deps=["eurofound-covid19-eu-policywatch"],
        key=("record_id",),
        temporal="end_date",
        sql='''
            SELECT
                CAST(record_id AS VARCHAR) AS record_id,
                identifier,
                title,
                country,
                category,
                subcategory,
                measure_type,
                status,
                date_type,
                sector_scope,
                social_partner_role,
                is_sector,
                is_occupation,
                CAST(try_strptime(NULLIF(start_date,  ''), '%m/%d/%Y') AS DATE) AS start_date,
                CAST(try_strptime(NULLIF(end_date,    ''), '%m/%d/%Y') AS DATE) AS end_date,
                CAST(try_strptime(NULLIF(last_update, ''), '%m/%d/%Y') AS DATE) AS last_update
            FROM "eurofound-covid19-eu-policywatch"
            WHERE record_id IS NOT NULL
        ''',
    ),
]
