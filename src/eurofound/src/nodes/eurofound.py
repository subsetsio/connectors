"""Eurofound connector — the two named statistical databases Eurofound publishes
as bulk files on its non-checkpoint CDNs (the public "data catalogue" itself is
locked behind a Vercel bot challenge and exposes only chart images, so it is not
machine-fetchable; see research/collect notes).

Subsets published:
  - collectively-agreed-wages-rates       (xlsx "Rates" sheet, ~198k obs)
  - collectively-agreed-wages-agreements  (xlsx "CollectiveAgreements" sheet)
  - collectively-agreed-wages-nace        (xlsx "NACE" sheet)
  - covid19-eu-policywatch                (covid19db.json, ~3167 measures)

Both source files are full snapshots fetched in one request — stateless full
re-pull every refresh (a few MB, no incremental filter exists).
"""

import io

import openpyxl
from subsets_utils import NodeSpec, get, save_raw_ndjson

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

NACE_MAP = {
    "CountryName": "country",
    "c_identifier_pbi": "agreement_id",
    "c_originalSector": "sector",
    "Code": "nace_code",
    "Description": "description",
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


def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


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


def _is_ca_id(value) -> bool:
    return isinstance(value, str) and value.startswith("CA-")


def fetch_mw_rates(node_id: str) -> None:
    rows = _read_sheet(_get_bytes(MW_XLSX_URL), "Rates", RATES_MAP)
    save_raw_ndjson(rows, node_id)


def fetch_mw_agreements(node_id: str) -> None:
    rows = [
        row
        for row in _read_sheet(_get_bytes(MW_XLSX_URL), "CollectiveAgreements", AGREEMENTS_MAP)
        if _is_ca_id(row.get("agreement_id")) and row.get("country")
    ]
    save_raw_ndjson(rows, node_id)


def fetch_mw_nace(node_id: str) -> None:
    rows = [
        row
        for row in _read_sheet(_get_bytes(MW_XLSX_URL), "NACE", NACE_MAP)
        if _is_ca_id(row.get("agreement_id")) and row.get("nace_code")
    ]
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
    NodeSpec(id="eurofound-collectively-agreed-wages-nace", fn=fetch_mw_nace, kind="download"),
    NodeSpec(id="eurofound-covid19-eu-policywatch", fn=fetch_covid_policywatch, kind="download"),
]
