"""bosai: per-office weather forecasts (long format)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet
from utils import BOSAI

_FORECAST_SCHEMA = pa.schema([
    ("office_code", pa.string()),
    ("publishing_office", pa.string()),
    ("report_datetime", pa.string()),
    ("area_code", pa.string()),
    ("area_name", pa.string()),
    ("element", pa.string()),
    ("valid_time", pa.string()),
    ("value", pa.string()),   # mixed: weather text, codes, pops, temps -> keep raw
])

# safety ceiling: JMA publishes ~58 forecast offices; a much larger count means
# the area taxonomy changed shape and the loop should be revisited, not silently
# truncated.
_MAX_OFFICES = 200


def fetch_weather_forecasts(node_id: str) -> None:
    offices = get(f"{BOSAI}/common/const/area.json", timeout=60).json().get("offices", {})
    office_codes = list(offices.keys())
    if len(office_codes) > _MAX_OFFICES:
        raise RuntimeError(
            f"{len(office_codes)} forecast offices exceeds ceiling {_MAX_OFFICES}; "
            "area taxonomy may have changed shape")

    rows = []
    fetched = 0
    for office in office_codes:
        resp = get(f"{BOSAI}/forecast/data/forecast/{office}.json", timeout=60)
        if resp.status_code == 404:
            # Not every office code serves a forecast document; skip those.
            continue
        resp.raise_for_status()
        reports = resp.json()
        fetched += 1
        for report in reports:
            pub = report.get("publishingOffice")
            report_dt = report.get("reportDatetime")
            for series in report.get("timeSeries", []):
                time_defines = series.get("timeDefines", [])
                for area in series.get("areas", []):
                    ainfo = area.get("area", {})
                    acode = ainfo.get("code")
                    aname = ainfo.get("name")
                    for elem, values in area.items():
                        if elem == "area" or not isinstance(values, list):
                            continue
                        for i, v in enumerate(values):
                            valid_time = time_defines[i] if i < len(time_defines) else None
                            rows.append({
                                "office_code": office,
                                "publishing_office": pub,
                                "report_datetime": report_dt,
                                "area_code": acode,
                                "area_name": aname,
                                "element": elem,
                                "valid_time": valid_time,
                                "value": None if v is None else str(v),
                            })
    if fetched == 0:
        raise RuntimeError("no forecast documents fetched; bosai forecast surface may have changed")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_FORECAST_SCHEMA), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="japan-meteorological-agency-weather-forecasts", fn=fetch_weather_forecasts, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="japan-meteorological-agency-weather-forecasts-transform",
        deps=["japan-meteorological-agency-weather-forecasts"],
        sql='''
            SELECT
                office_code,
                publishing_office,
                CAST(report_datetime AS TIMESTAMPTZ) AS report_datetime,
                area_code, area_name, element,
                CAST(valid_time AS TIMESTAMPTZ) AS valid_time,
                value
            FROM "japan-meteorological-agency-weather-forecasts"
            WHERE area_code IS NOT NULL AND element IS NOT NULL AND valid_time IS NOT NULL
        ''',
    ),
]
