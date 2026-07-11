"""NCD Risk Factor Collaboration (NCD-RisC) connector.

NCD-RisC publishes pooled global modelling estimates for major non-communicable
disease risk factors (adiposity/BMI, diabetes, blood pressure, cholesterol,
child & adolescent height, hypertension) as a fixed set of CSV/ZIP files served
from https://www.ncdrisc.org/downloads/. There is no API and no incremental
query surface — each file is a complete, self-contained table, re-published as a
new path only when a risk factor is re-analysed. So every asset is a stateless
full re-pull: download the file, overwrite. No watermark, no cursor.

Each source file is a wide table whose dimension columns (area, ISO, sex, year,
age) vary slightly and whose many estimate columns differ entirely per risk
factor. To keep the published tables uniform and the SQL transforms thin, the
fetch fn melts every file into one canonical long shape:

    area | iso | sex | year | age | metric | value

`metric` carries the original estimate column name (e.g. "Prevalence of
diabetes lower 95% uncertainty interval"); `value` is the float (source "NA" ->
null). Sex is taken from the file's Sex column, or inferred from the filename
for the per-sex blood-pressure files that omit it. Age is the file's Age / Age
group column, or derived from the filename (age-standardised vs crude) when the
file has no age dimension.

Four assets are ZIP archives bundling a single member CSV; the fetch fn unzips
in-memory and treats the member exactly like a plain CSV.
"""
import csv
import io
import json
import zipfile


from subsets_utils import (
    NodeSpec,
    get,
    raw_writer,
    transient_retry,
)

BASE = "https://www.ncdrisc.org/"

# entity id (== collect catalog id) -> relative download path
ENTITY_PATHS = {
    "ncd-risc-lancet-2017-bp-age-standardised-countries": "downloads/bp/NCD_RisC_Lancet_2017_BP_age_standardised_countries.csv",
    "ncd-risc-lancet-2017-bp-age-standardised-regions": "downloads/bp/NCD_RisC_Lancet_2017_BP_age_standardised_regions.csv",
    "ncd-risc-lancet-2017-bp-age-standardised-world": "downloads/bp/NCD_RisC_Lancet_2017_BP_age_standardised_world.csv",
    "ncd-risc-lancet-2017-bp-crude-countries": "downloads/bp/NCD_RisC_Lancet_2017_BP_crude_countries.csv",
    "ncd-risc-lancet-2017-bp-crude-regions": "downloads/bp/NCD_RisC_Lancet_2017_BP_crude_regions.csv",
    "ncd-risc-lancet-2017-bp-crude-world": "downloads/bp/NCD_RisC_Lancet_2017_BP_crude_world.csv",
    "ncd-risc-lancet-2017-men-agespecific-mean-dbp-by-country": "downloads/bp/NCD_RisC_Lancet_2017_Men_Agespecific_Mean_DBP_by_Country.csv",
    "ncd-risc-lancet-2017-men-agespecific-mean-sbp-by-country": "downloads/bp/NCD_RisC_Lancet_2017_Men_Agespecific_Mean_SBP_by_Country.csv",
    "ncd-risc-lancet-2017-women-agespecific-mean-dbp-by-country": "downloads/bp/NCD_RisC_Lancet_2017_Women_Agespecific_Mean_DBP_by_Country.csv",
    "ncd-risc-lancet-2017-women-agespecific-mean-sbp-by-country": "downloads/bp/NCD_RisC_Lancet_2017_Women_Agespecific_Mean_SBP_by_Country.csv",
    "ncd-risc-lancet-2020-height-child-adolescent-country": "downloads/bmi-height-2020/height/all_countries/NCD_RisC_Lancet_2020_height_child_adolescent_country.zip",
    "ncd-risc-lancet-2020-height-child-adolescent-global": "downloads/bmi-height-2020/height/global/NCD_RisC_Lancet_2020_height_child_adolescent_global.csv",
    "ncd-risc-lancet-2020-height-child-adolescent-region": "downloads/bmi-height-2020/height/regional/NCD_RisC_Lancet_2020_height_child_adolescent_region.csv",
    "ncd-risc-lancet-2021-hypertension-age-specific-estimates-by-country": "downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_age_specific_estimates_by_country.csv",
    "ncd-risc-lancet-2021-hypertension-age-standardised-countries": "downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_countries.csv",
    "ncd-risc-lancet-2021-hypertension-age-standardised-regions": "downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_regions.csv",
    "ncd-risc-lancet-2021-hypertension-age-standardised-world": "downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_world.csv",
    "ncd-risc-lancet-2021-hypertension-crude-countries": "downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_countries.csv",
    "ncd-risc-lancet-2021-hypertension-crude-regions": "downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_regions.csv",
    "ncd-risc-lancet-2021-hypertension-crude-world": "downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_world.csv",
    "ncd-risc-lancet-2024-diabetes-age-specific-countries": "downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_specific_countries.zip",
    "ncd-risc-lancet-2024-diabetes-age-standardised-countries": "downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_countries.csv",
    "ncd-risc-lancet-2024-diabetes-age-standardised-regions": "downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_regions.csv",
    "ncd-risc-lancet-2024-diabetes-age-standardised-world": "downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_world.csv",
    "ncd-risc-lancet-2024-diabetes-crude-countries": "downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_countries.csv",
    "ncd-risc-lancet-2024-diabetes-crude-regions": "downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_regions.csv",
    "ncd-risc-lancet-2024-diabetes-crude-world": "downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_world.csv",
    "ncd-risc-nature-2020-cholesterol-age-specific-countries": "downloads/chol/NCD_RisC_Nature_2020_Cholesterol_age_specific_countries.csv",
    "ncd-risc-nature-2020-cholesterol-age-standardised-countries": "downloads/chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_countries.csv",
    "ncd-risc-nature-2020-cholesterol-age-standardised-regions": "downloads/chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_regions.csv",
    "ncd-risc-nature-2020-cholesterol-age-standardised-world": "downloads/chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_world.csv",
    "ncd-risc-nature-2026-bmi-age-standardised-country": "downloads/bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_country.csv",
    "ncd-risc-nature-2026-bmi-age-standardised-region": "downloads/bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_region.csv",
    "ncd-risc-nature-2026-bmi-age-standardised-world": "downloads/bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_world.csv",
    "ncd-risc-nature-2026-bmi-female-age-specific-country": "downloads/bmi-2026/adult/NCD_RisC_Nature_2026_BMI_female_age_specific_country.zip",
    "ncd-risc-nature-2026-bmi-male-age-specific-country": "downloads/bmi-2026/adult/NCD_RisC_Nature_2026_BMI_male_age_specific_country.zip",
}

ENTITY_IDS = list(ENTITY_PATHS)

# Dimension columns, matched case-insensitively after header cleaning. Anything
# not in here is treated as an estimate column and melted into metric/value.
_AREA_COLS = {"country/region/world", "country", "region", "country/region"}
_AGE_COLS = {"age", "age group", "agegroup"}


# ---- HTTP ------------------------------------------------------------------


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


# ---- parsing / normalisation ----------------------------------------------

def _clean_header(name: str) -> str:
    """Strip BOM and surrounding quotes some NCD-RisC files carry on the first
    column (e.g. '﻿"Year"')."""
    return name.replace("﻿", "").strip().strip('"').strip()


def _infer_sex(entity_id: str) -> str | None:
    low = entity_id.lower()
    if "women" in low or "female" in low:
        return "Women"
    if "men" in low or "male" in low:
        return "Men"
    return None


def _default_age(entity_id: str) -> str | None:
    low = entity_id.lower()
    if "crude" in low:
        return "Crude"
    if "age-standardised" in low or "age_standardised" in low:
        return "Age-standardised"
    return None


def _default_area(entity_id: str) -> str | None:
    low = entity_id.lower()
    if "global" in low or "world" in low:
        return "World"
    return None


def _to_float(raw: str):
    s = (raw or "").strip()
    if s == "" or s.upper() == "NA" or s.upper() == "NAN":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _melt_csv(text: str, entity_id: str):
    """Yield one long-format dict per (source row x estimate column)."""
    reader = csv.reader(io.StringIO(text))
    rows = iter(reader)
    try:
        header = [_clean_header(h) for h in next(rows)]
    except StopIteration:
        return
    lower = [h.lower() for h in header]

    # locate dimension columns by index
    idx = {"area": None, "iso": None, "sex": None, "year": None, "age": None}
    metric_cols = []  # (col_index, original_name)
    for i, h in enumerate(lower):
        if h in _AREA_COLS and idx["area"] is None:
            idx["area"] = i
        elif h == "iso" and idx["iso"] is None:
            idx["iso"] = i
        elif h == "sex" and idx["sex"] is None:
            idx["sex"] = i
        elif h == "year" and idx["year"] is None:
            idx["year"] = i
        elif h in _AGE_COLS and idx["age"] is None:
            idx["age"] = i
        else:
            metric_cols.append((i, header[i]))

    sex_fallback = _infer_sex(entity_id)
    age_fallback = _default_age(entity_id)
    area_fallback = _default_area(entity_id)

    def cell(row, i):
        if i is None or i >= len(row):
            return None
        v = row[i].strip()
        return v if v not in ("", "NA") else None

    for row in rows:
        if not row:
            continue
        area = cell(row, idx["area"]) or area_fallback
        iso = cell(row, idx["iso"])
        sex = cell(row, idx["sex"]) or sex_fallback
        year_raw = cell(row, idx["year"])
        try:
            year = int(float(year_raw)) if year_raw is not None else None
        except ValueError:
            year = None
        age = cell(row, idx["age"]) or age_fallback
        for ci, metric_name in metric_cols:
            if ci >= len(row):
                continue
            value = _to_float(row[ci])
            yield {
                "area": area,
                "iso": iso,
                "sex": sex,
                "year": year,
                "age": age,
                "metric": metric_name,
                "value": value,
            }


def _csv_texts(content: bytes, path: str):
    """Return the CSV text(s) inside a download — unzipping if needed."""
    if path.lower().endswith(".zip"):
        zf = zipfile.ZipFile(io.BytesIO(content))
        members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not members:
            raise AssertionError(f"{path}: zip contains no CSV members")
        for name in members:
            yield zf.read(name).decode("utf-8", errors="replace")
    else:
        yield content.decode("utf-8", errors="replace")


# ---- fetch -----------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id is the asset name
    entity_id = node_id[len("ncd-risc-"):]  # recover the collect entity id
    path = ENTITY_PATHS[entity_id]
    content = _fetch_bytes(BASE + path)

    # Stream melted rows straight to disk; the age-specific files melt to a few
    # million long rows, too large to hold in memory comfortably.
    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for text in _csv_texts(content, path):
            for rec in _melt_csv(text, entity_id):
                f.write(json.dumps(rec) + "\n")
                n += 1
    if n == 0:
        raise AssertionError(f"{asset}: produced 0 long rows from {path}")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ncd-risc-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
