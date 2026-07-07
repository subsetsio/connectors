import csv
import io
import json

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet


BASE_URL = (
    "https://reutersinstitute.politics.ox.ac.uk/modules/custom/"
    "olamalu_reuters_dnr_infographics/data"
)
REFERENCE_URL = f"{BASE_URL}/reference.en.json"


def _json_or_none(value) -> str | None:
    if value is None:
        return None
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def _reference() -> dict:
    resp = get(REFERENCE_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _csv_rows(url: str) -> list[dict]:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    text = resp.content.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def _float_or_none(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _int_or_none(value: str | None) -> int | None:
    if value in (None, ""):
        return None
    return int(float(value))


SURVEY_SCHEMA = pa.schema(
    [
        ("question_id", pa.string()),
        ("year", pa.int64()),
        ("country_code", pa.string()),
        ("option_id", pa.string()),
        ("split_var", pa.string()),
        ("split_value", pa.string()),
        ("pct", pa.float64()),
        ("base_unwt_calc", pa.int64()),
    ]
)


def fetch_survey_observations(node_id: str) -> None:
    ref = _reference()
    rows = []
    for question_id in sorted((ref.get("questions") or {}).keys()):
        url = f"{BASE_URL}/{question_id.lower()}/markets.csv"
        for row in _csv_rows(url):
            rows.append(
                {
                    "question_id": question_id,
                    "year": _int_or_none(row.get("year")),
                    "country_code": row.get("country_code") or None,
                    "option_id": row.get("option_id") or None,
                    "split_var": row.get("split_var") or None,
                    "split_value": row.get("split_value") or None,
                    "pct": _float_or_none(row.get("pct")),
                    "base_unwt_calc": _int_or_none(row.get("base_unwt_calc")),
                }
            )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SURVEY_SCHEMA), node_id)


QUESTIONS_SCHEMA = pa.schema(
    [
        ("question_id", pa.string()),
        ("question_label", pa.string()),
        ("question_text", pa.string()),
        ("response_type", pa.string()),
        ("methodology", pa.string()),
        ("option_id", pa.string()),
        ("option_label", pa.string()),
        ("option_display_exclusions_json", pa.string()),
        ("question_display_exclusions_json", pa.string()),
        ("demog_exclusions_json", pa.string()),
        ("market_basket_label", pa.string()),
        ("market_basket_count", pa.string()),
    ]
)


def fetch_questions(node_id: str) -> None:
    ref = _reference()
    rows = []
    for question_id, question in sorted((ref.get("questions") or {}).items()):
        for option in question.get("options") or []:
            rows.append(
                {
                    "question_id": question_id,
                    "question_label": question.get("question_label"),
                    "question_text": question.get("question_text"),
                    "response_type": question.get("response_type"),
                    "methodology": question.get("methodology"),
                    "option_id": option.get("id"),
                    "option_label": option.get("label"),
                    "option_display_exclusions_json": _json_or_none(
                        option.get("display_exclusions")
                    ),
                    "question_display_exclusions_json": _json_or_none(
                        question.get("display_exclusions")
                    ),
                    "demog_exclusions_json": _json_or_none(
                        question.get("demog_exclusions")
                    ),
                    "market_basket_label": question.get("market_basket_label"),
                    "market_basket_count": question.get("market_basket_count"),
                }
            )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=QUESTIONS_SCHEMA), node_id)


MARKETS_SCHEMA = pa.schema(
    [
        ("market_code", pa.string()),
        ("name", pa.string()),
        ("all_markets", pa.bool_()),
    ]
)


def fetch_markets(node_id: str) -> None:
    ref = _reference()
    rows = [
        {
            "market_code": code,
            "name": market.get("name"),
            "all_markets": bool(market.get("all_markets", False)),
        }
        for code, market in sorted((ref.get("markets") or {}).items())
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=MARKETS_SCHEMA), node_id)


DEMOGRAPHICS_SCHEMA = pa.schema(
    [
        ("demographic_id", pa.string()),
        ("question_label", pa.string()),
        ("question_text", pa.string()),
        ("option_id", pa.string()),
        ("option_label", pa.string()),
        ("display_exclusions_json", pa.string()),
    ]
)


def fetch_demographics(node_id: str) -> None:
    ref = _reference()
    rows = []
    for demographic_id, demographic in sorted((ref.get("demographics") or {}).items()):
        for option in demographic.get("options") or []:
            rows.append(
                {
                    "demographic_id": demographic_id,
                    "question_label": demographic.get("question_label"),
                    "question_text": demographic.get("question_text"),
                    "option_id": option.get("id"),
                    "option_label": option.get("label"),
                    "display_exclusions_json": _json_or_none(
                        demographic.get("display_exclusions")
                    ),
                }
            )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=DEMOGRAPHICS_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="reuters-institute-demographics",
        fn=fetch_demographics,
        kind="download",
    ),
    NodeSpec(
        id="reuters-institute-markets",
        fn=fetch_markets,
        kind="download",
    ),
    NodeSpec(
        id="reuters-institute-questions",
        fn=fetch_questions,
        kind="download",
    ),
    NodeSpec(
        id="reuters-institute-survey-observations",
        fn=fetch_survey_observations,
        kind="download",
    ),
]
