"""CAPMAS (Central Agency for Public Mobilization and Statistics, Egypt) connector.

Source: the official capmas.gov.eg statistics REST API (the backend of the React
site, reverse-engineered — no public docs). JSON envelope {"data": ..., "state": bool}.
Base: https://www.capmas.gov.eg:8080/api  (non-standard :8080 port, no auth).

Catalog tree: 3 main subjects -> ~24 sub-subjects (Subject/HasData) -> publications
-> indicators (Subject/SubSubjectWithIndicator/{subSubjectId}). Each indicator's full
data is one GET: Indicator/IndicatorFilter?IndicatorId={indicatorId}&SubSubjectId={ssId}
returning a list of breakdown categories, each with a data[] of {value,year,quarter,month}.
Per-indicator units/periodicity come from Indicator/IndicatorDetails?indicatorId=&publicationId=.

Three published tables (the World-Bank shape for an indicator API):
  - eg-capmas-subjects    : the two-level subject taxonomy (reference).
  - eg-capmas-indicators  : one row per indicator with units / periodicity / coverage (reference).
  - eg-capmas-values      : long-format observations across ALL indicators (the corpus).

Fetch shape: stateless full re-pull every run (no bulk export exists; ~7.4k indicators,
one request each, ~11 req/s measured -> ~10-15 min per heavy spec). English labels live
in the *Translations arrays (top-level fields stay Arabic even with the 'lo: en' header),
so we extract en explicitly and fall back to Arabic.
"""
import pyarrow as pa
import httpx
from subsets_utils import (
    NodeSpec, get, transient_retry,
    save_raw_parquet, raw_parquet_writer,
)

BASE = "https://www.capmas.gov.eg:8080/api"
HEADERS = {"lo": "en"}            # ASCII-only; selects English translations
VALUES_FLUSH_EVERY = 250          # indicators per parquet row-group flush (bounded memory)


@transient_retry(attempts=8, max_wait=90)
def _get_json(path: str) -> dict:
    resp = get(f"{BASE}/{path}", headers=HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _data(path: str):
    return _get_json(path)["data"]


def _en(translations, key, fallback=None):
    """English value from a *Translations list (locale=='en'); else fallback."""
    for t in translations or []:
        if t.get("locale") == "en" and t.get(key):
            return t[key]
    return fallback


def _enumerate_indicators():
    """Walk the subject tree -> one record per indicator, deduped by indicator_id
    (first occurrence wins). Carries the grouping + the (sub_subject_id, publication_id)
    needed to fetch the indicator's metadata and values."""
    tree = _data("Subject/HasData")
    seen = {}
    for main in tree:
        main_id = main["id"]
        main_en = _en(main.get("subjectTranslations"), "title", main.get("title"))
        main_ar = main.get("title")
        for ss in main.get("subSubjects", []) or []:
            ss_id = ss["id"]
            ss_en = _en(ss.get("subjectTranslations"), "title", ss.get("title"))
            detail = _data("Subject/SubSubjectWithIndicator/%s" % ss_id)
            for pub in detail.get("publicationWithIndicators", []) or []:
                pub_id = pub["id"]
                pub_ar = pub.get("name")
                pub_en = _en(pub.get("publicationTranslations"), "title", pub_ar)
                for ind in pub.get("indicators", []) or []:
                    iid = ind["indicatorId"]
                    if iid in seen:
                        continue
                    seen[iid] = {
                        "indicator_id": iid,
                        "name_ar": ind.get("name"),
                        "name_en": _en(ind.get("indicatorTranslations"), "name", ind.get("name")),
                        "main_subject_id": main_id,
                        "main_subject_en": main_en,
                        "main_subject_ar": main_ar,
                        "sub_subject_id": ss_id,
                        "sub_subject_en": ss_en,
                        "sub_subject_ar": ss.get("title"),
                        "publication_id": pub_id,
                        "publication_en": pub_en,
                        "publication_ar": pub_ar,
                    }
    return list(seen.values())


def _is_permanent_http(exc) -> bool:
    return (
        isinstance(exc, httpx.HTTPStatusError)
        and 400 <= exc.response.status_code < 500
        and exc.response.status_code != 429
    )


# --------------------------------------------------------------------------- #
#  subjects — two-level taxonomy (1 request)
# --------------------------------------------------------------------------- #
SUBJECTS_SCHEMA = pa.schema([
    ("main_subject_id", pa.int64()),
    ("main_subject_en", pa.string()),
    ("main_subject_ar", pa.string()),
    ("sub_subject_id", pa.int64()),
    ("sub_subject_en", pa.string()),
    ("sub_subject_ar", pa.string()),
])


def fetch_subjects(node_id: str) -> None:
    asset = node_id
    tree = _data("Subject/HasData")
    rows = []
    for main in tree:
        main_en = _en(main.get("subjectTranslations"), "title", main.get("title"))
        for ss in main.get("subSubjects", []) or []:
            rows.append({
                "main_subject_id": main["id"],
                "main_subject_en": main_en,
                "main_subject_ar": main.get("title"),
                "sub_subject_id": ss["id"],
                "sub_subject_en": _en(ss.get("subjectTranslations"), "title", ss.get("title")),
                "sub_subject_ar": ss.get("title"),
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SUBJECTS_SCHEMA), asset)


# --------------------------------------------------------------------------- #
#  indicators — one row per indicator + units / periodicity / coverage
# --------------------------------------------------------------------------- #
INDICATORS_SCHEMA = pa.schema([
    ("indicator_id", pa.int64()),
    ("name_en", pa.string()),
    ("name_ar", pa.string()),
    ("main_subject_id", pa.int64()),
    ("main_subject_en", pa.string()),
    ("sub_subject_id", pa.int64()),
    ("sub_subject_en", pa.string()),
    ("publication_id", pa.int64()),
    ("publication_en", pa.string()),
    ("publication_ar", pa.string()),
    ("periodicity_en", pa.string()),
    ("measure_unit_en", pa.string()),
    ("measure_unit_ar", pa.string()),
    ("start_year", pa.int64()),
    ("end_year", pa.int64()),
])


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    indicators = _enumerate_indicators()
    rows = []
    for rec in indicators:
        iid, pid = rec["indicator_id"], rec["publication_id"]
        periodicity = unit_en = unit_ar = start_year = end_year = None
        try:
            det = _data("Indicator/IndicatorDetails?indicatorId=%s&publicationId=%s" % (iid, pid))
            periodic = det.get("periodic") or {}
            periodicity = _en(periodic.get("periodicTranslations"), "name", periodic.get("name"))
            mu = det.get("measureUnit") or {}
            unit_ar = mu.get("name")
            unit_en = _en(mu.get("measureUnitTranslations"), "name", unit_ar)
            start_year = (det.get("startPeriod") or {}).get("year")
            end_year = (det.get("endPeriod") or {}).get("year")
        except Exception as exc:  # noqa: BLE001
            if not _is_permanent_http(exc):
                raise
            print("  skip IndicatorDetails iid=%s pub=%s: %s" % (iid, pid, type(exc).__name__))
        rows.append({
            "indicator_id": iid,
            "name_en": rec["name_en"],
            "name_ar": rec["name_ar"],
            "main_subject_id": rec["main_subject_id"],
            "main_subject_en": rec["main_subject_en"],
            "sub_subject_id": rec["sub_subject_id"],
            "sub_subject_en": rec["sub_subject_en"],
            "publication_id": pid,
            "publication_en": rec["publication_en"],
            "publication_ar": rec["publication_ar"],
            "periodicity_en": periodicity,
            "measure_unit_en": unit_en,
            "measure_unit_ar": unit_ar,
            "start_year": start_year,
            "end_year": end_year,
        })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=INDICATORS_SCHEMA), asset)


# --------------------------------------------------------------------------- #
#  values — long-format observations across all indicators
# --------------------------------------------------------------------------- #
VALUES_SCHEMA = pa.schema([
    ("main_subject_id", pa.int64()),
    ("sub_subject_id", pa.int64()),
    ("indicator_id", pa.int64()),
    ("indicator_name_en", pa.string()),
    ("category_id", pa.int64()),
    ("category_en", pa.string()),
    ("category_ar", pa.string()),
    ("year", pa.int64()),
    ("quarter", pa.int64()),
    ("month", pa.int64()),
    ("value", pa.float64()),
])


def fetch_values(node_id: str) -> None:
    asset = node_id
    indicators = _enumerate_indicators()
    buf = []
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        def flush():
            if buf:
                writer.write_table(pa.Table.from_pylist(buf, schema=VALUES_SCHEMA))
                buf.clear()

        for i, rec in enumerate(indicators):
            iid, ss_id = rec["indicator_id"], rec["sub_subject_id"]
            try:
                series = _data("Indicator/IndicatorFilter?IndicatorId=%s&SubSubjectId=%s" % (iid, ss_id))
            except Exception as exc:  # noqa: BLE001
                if not _is_permanent_http(exc):
                    raise
                print("  skip IndicatorFilter iid=%s ss=%s: %s" % (iid, ss_id, type(exc).__name__))
                series = []
            for cat in series or []:
                cat_en = _en(cat.get("filterTranslations"), "name", cat.get("name"))
                for pt in cat.get("data", []) or []:
                    buf.append({
                        "main_subject_id": rec["main_subject_id"],
                        "sub_subject_id": ss_id,
                        "indicator_id": iid,
                        "indicator_name_en": rec["name_en"],
                        "category_id": cat.get("id"),
                        "category_en": cat_en,
                        "category_ar": cat.get("name"),
                        "year": pt.get("year"),
                        "quarter": pt.get("quarter"),
                        "month": pt.get("month"),
                        "value": pt.get("value"),
                    })
            if (i + 1) % VALUES_FLUSH_EVERY == 0:
                flush()
        flush()


# --------------------------------------------------------------------------- #
#  Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="eg-capmas-subjects", fn=fetch_subjects, kind="download"),
    NodeSpec(id="eg-capmas-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="eg-capmas-values", fn=fetch_values, kind="download"),
]
