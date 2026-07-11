"""NOAA/NCEI International Tree-Ring Data Bank catalog connector.

The accepted first publication scope is the Paleo Search catalog metadata:
studies, sites, and data-file manifests. Tree-ring payload parsing is deferred
because the source exposes tens of thousands of domain-format files.
"""

from __future__ import annotations

from datetime import date
import json
from pathlib import PurePosixPath

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

CATALOG_URL = "https://www.ncei.noaa.gov/access/paleo-search/study/search.json"
CATALOG_PARAMS = {"dataTypeId": "18", "limit": "100000"}

_STUDIES_SCHEMA = pa.schema([
    ("study_id", pa.string()),
    ("xml_id", pa.string()),
    ("uuid", pa.string()),
    ("entry_id", pa.string()),
    ("study_name", pa.string()),
    ("study_code", pa.string()),
    ("doi", pa.string()),
    ("data_publisher", pa.string()),
    ("data_type", pa.string()),
    ("investigators", pa.string()),
    ("version", pa.string()),
    ("study_notes", pa.string()),
    ("online_resource_link", pa.string()),
    ("dif_metadata_link", pa.string()),
    ("iso_metadata_link", pa.string()),
    ("original_source", pa.string()),
    ("data_type_information", pa.string()),
    ("reconstruction", pa.string()),
    ("contribution_date", pa.date32()),
    ("earliest_year_bp", pa.int64()),
    ("most_recent_year_bp", pa.int64()),
    ("earliest_year_ce", pa.int64()),
    ("most_recent_year_ce", pa.int64()),
    ("science_keywords_json", pa.string()),
    ("funding_json", pa.string()),
    ("publication_json", pa.string()),
    ("reference_json", pa.string()),
    ("data_license_description", pa.string()),
    ("data_license_url", pa.string()),
])

_SITES_SCHEMA = pa.schema([
    ("study_id", pa.string()),
    ("site_id", pa.string()),
    ("site_name", pa.string()),
    ("site_code", pa.string()),
    ("mappable", pa.string()),
    ("location_name", pa.string()),
    ("geo_type", pa.string()),
    ("geometry_type", pa.string()),
    ("geometry_coordinates_json", pa.string()),
    ("southernmost_latitude", pa.float64()),
    ("northernmost_latitude", pa.float64()),
    ("westernmost_longitude", pa.float64()),
    ("easternmost_longitude", pa.float64()),
    ("min_elevation_meters", pa.float64()),
    ("max_elevation_meters", pa.float64()),
    ("study_contribution_date", pa.date32()),
])

_DATA_FILES_SCHEMA = pa.schema([
    ("study_id", pa.string()),
    ("site_id", pa.string()),
    ("data_table_id", pa.string()),
    ("data_table_name", pa.string()),
    ("file_url", pa.string()),
    ("url_description", pa.string()),
    ("link_text", pa.string()),
    ("file_extension", pa.string()),
    ("time_unit", pa.string()),
    ("earliest_year", pa.int64()),
    ("most_recent_year", pa.int64()),
    ("earliest_year_bp", pa.int64()),
    ("most_recent_year_bp", pa.int64()),
    ("earliest_year_ce", pa.int64()),
    ("most_recent_year_ce", pa.int64()),
    ("core_length_meters", pa.float64()),
    ("data_table_notes", pa.string()),
    ("species_json", pa.string()),
    ("variables_json", pa.string()),
    ("noaa_keywords_json", pa.string()),
    ("study_contribution_date", pa.date32()),
])


def _json(value) -> str | None:
    if value in (None, [], {}):
        return None
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _str(value) -> str | None:
    if value is None:
        return None
    return str(value)


def _int(value) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _float(value) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _date(value) -> date | None:
    if not value:
        return None
    return date.fromisoformat(str(value)[:10])


def _fetch_studies() -> list[dict]:
    resp = get(CATALOG_URL, params=CATALOG_PARAMS, timeout=(10.0, 300.0))
    resp.raise_for_status()
    payload = resp.json()
    studies = payload.get("study") or []
    if len(studies) < 8000:
        raise RuntimeError(f"Paleo Search returned only {len(studies)} tree-ring studies")
    return studies


def _file_extension(url: str | None) -> str | None:
    if not url:
        return None
    suffix = PurePosixPath(url).suffix.lower()
    return suffix[1:] if suffix.startswith(".") else suffix or None


def _study_row(study: dict) -> dict:
    return {
        "study_id": _str(study.get("NOAAStudyId")),
        "xml_id": _str(study.get("xmlId")),
        "uuid": _str(study.get("uuid")),
        "entry_id": _str(study.get("entryId")),
        "study_name": _str(study.get("studyName")),
        "study_code": _str(study.get("studyCode")),
        "doi": _str(study.get("doi")),
        "data_publisher": _str(study.get("dataPublisher")),
        "data_type": _str(study.get("dataType")),
        "investigators": _str(study.get("investigators")),
        "version": _str(study.get("version")),
        "study_notes": _str(study.get("studyNotes")),
        "online_resource_link": _str(study.get("onlineResourceLink")),
        "dif_metadata_link": _str(study.get("difMetadataLink")),
        "iso_metadata_link": _str(study.get("isoMetadataLink")),
        "original_source": _str(study.get("originalSource")),
        "data_type_information": _str(study.get("dataTypeInformation")),
        "reconstruction": _str(study.get("reconstruction")),
        "contribution_date": _date(study.get("contributionDate")),
        "earliest_year_bp": _int(study.get("earliestYearBP")),
        "most_recent_year_bp": _int(study.get("mostRecentYearBP")),
        "earliest_year_ce": _int(study.get("earliestYearCE")),
        "most_recent_year_ce": _int(study.get("mostRecentYearCE")),
        "science_keywords_json": _json(study.get("scienceKeywords")),
        "funding_json": _json(study.get("funding")),
        "publication_json": _json(study.get("publication")),
        "reference_json": _json(study.get("reference")),
        "data_license_description": _str(study.get("dataLicenseDescription")),
        "data_license_url": _str(study.get("dataLicenseUrl")),
    }


def _site_rows(study: dict) -> list[dict]:
    rows = []
    for site in study.get("site") or []:
        geo = site.get("geo") or {}
        geometry = geo.get("geometry") or {}
        props = geo.get("properties") or {}
        rows.append({
            "study_id": _str(study.get("NOAAStudyId")),
            "site_id": _str(site.get("NOAASiteId")),
            "site_name": _str(site.get("siteName")),
            "site_code": _str(site.get("siteCode")),
            "mappable": _str(site.get("mappable")),
            "location_name": _str(site.get("locationName")),
            "geo_type": _str(geo.get("geoType")),
            "geometry_type": _str(geometry.get("type")),
            "geometry_coordinates_json": _json(geometry.get("coordinates")),
            "southernmost_latitude": _float(props.get("southernmostLatitude")),
            "northernmost_latitude": _float(props.get("northernmostLatitude")),
            "westernmost_longitude": _float(props.get("westernmostLongitude")),
            "easternmost_longitude": _float(props.get("easternmostLongitude")),
            "min_elevation_meters": _float(props.get("minElevationMeters")),
            "max_elevation_meters": _float(props.get("maxElevationMeters")),
            "study_contribution_date": _date(study.get("contributionDate")),
        })
    return rows


def _data_file_rows(study: dict) -> list[dict]:
    rows = []
    for site in study.get("site") or []:
        for table in site.get("paleoData") or []:
            for data_file in table.get("dataFile") or []:
                rows.append({
                    "study_id": _str(study.get("NOAAStudyId")),
                    "site_id": _str(site.get("NOAASiteId")),
                    "data_table_id": _str(table.get("NOAADataTableId")),
                    "data_table_name": _str(table.get("dataTableName")),
                    "file_url": _str(data_file.get("fileUrl")),
                    "url_description": _str(data_file.get("urlDescription")),
                    "link_text": _str(data_file.get("linkText")),
                    "file_extension": _file_extension(data_file.get("fileUrl")),
                    "time_unit": _str(table.get("timeUnit")),
                    "earliest_year": _int(table.get("earliestYear")),
                    "most_recent_year": _int(table.get("mostRecentYear")),
                    "earliest_year_bp": _int(table.get("earliestYearBP")),
                    "most_recent_year_bp": _int(table.get("mostRecentYearBP")),
                    "earliest_year_ce": _int(table.get("earliestYearCE")),
                    "most_recent_year_ce": _int(table.get("mostRecentYearCE")),
                    "core_length_meters": _float(table.get("coreLengthMeters")),
                    "data_table_notes": _str(table.get("dataTableNotes")),
                    "species_json": _json(table.get("species")),
                    "variables_json": _json(data_file.get("variables")),
                    "noaa_keywords_json": _json(data_file.get("NOAAKeywords")),
                    "study_contribution_date": _date(study.get("contributionDate")),
                })
    return rows


def fetch_catalog(node_id: str) -> None:
    studies = _fetch_studies()
    if node_id == "itrdb-studies":
        rows = [_study_row(study) for study in studies]
        table = pa.Table.from_pylist(rows, schema=_STUDIES_SCHEMA)
    elif node_id == "itrdb-sites":
        rows = [row for study in studies for row in _site_rows(study)]
        table = pa.Table.from_pylist(rows, schema=_SITES_SCHEMA)
    elif node_id == "itrdb-data-files":
        rows = [row for study in studies for row in _data_file_rows(study)]
        table = pa.Table.from_pylist(rows, schema=_DATA_FILES_SCHEMA)
    else:
        raise ValueError(f"unknown ITRDB node id: {node_id}")
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="itrdb-data-files", fn=fetch_catalog, kind="download"),
    NodeSpec(id="itrdb-sites", fn=fetch_catalog, kind="download"),
    NodeSpec(id="itrdb-studies", fn=fetch_catalog, kind="download"),
]
