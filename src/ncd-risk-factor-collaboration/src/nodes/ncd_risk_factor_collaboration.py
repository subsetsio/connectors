"""NCD Risk Factor Collaboration (NCD-RisC) connector.

NCD-RisC publishes pooled-analysis estimates for a handful of distinct risk
factors as static CSV files at stable /downloads/ URLs (no auth). Each risk
factor is one published Delta table.

Within a risk factor the world / region / country files and the
age-standardised / crude files all share the SAME indicator columns; they
differ only in dimension *values* (the geography, and the "Age" column which
carries "Age-standardised" vs "Crude"). The column ORDER and the presence of an
"Age"/"Age group" column vary between files, so columns are detected by NAME,
never by position.

Every fetch fn normalizes its risk factor's CSVs into one UNIFORM tidy
long-format schema (see SCHEMA): one row per (entity, sex, year, age,
indicator). The wide indicator triples (central / lower 95% / upper 95%) are
unpivoted so that adding or dropping an indicator never changes the schema.

Strategy: stateless full re-pull. The whole corpus is a few dozen small CSVs
(< 1 GB total); estimates are republished as whole releases every few years, and
there is no incremental filter, so every run re-fetches and overwrites.
"""

import io
import zipfile

import httpx
import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

PREFIX = "ncd-risk-factor-collaboration-"
BASE = "https://www.ncdrisc.org/downloads"

# Uniform output schema for every risk factor (tidy long format).
SCHEMA = pa.schema([
    ("entity", pa.string()),            # country / region / "World" label
    ("iso", pa.string()),               # ISO3 for countries, null otherwise
    ("sex", pa.string()),
    ("year", pa.int64()),
    ("age", pa.string()),               # "Age-standardised" / "Crude" / age group / null
    ("geographic_level", pa.string()),  # country | region | world
    ("indicator", pa.string()),         # central-estimate column name (incl. unit)
    ("value", pa.float64()),
    ("lower_95", pa.float64()),
    ("upper_95", pa.float64()),
])

# Per risk factor: the source files to union. Each is (path, level, kind).
# kind "csv" = a direct CSV; "zip" = a zip archive of per-country CSVs.
# Filenames verified from the ncdrisc.org data-download pages.
FILES = {
    "adult-bmi": [
        ("bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_country.csv", "country", "csv"),
        ("bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_region.csv", "region", "csv"),
        ("bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_world.csv", "world", "csv"),
    ],
    "child-adolescent-bmi": [
        ("bmi-2026/child_ado/NCD_RisC_Nature_2026_BMI_child_adolescent_country_ageStd.csv", "country", "csv"),
        ("bmi-2026/child_ado/NCD_RisC_Nature_2026_BMI_child_adolescent_region.csv", "region", "csv"),
        ("bmi-2026/child_ado/NCD_RisC_Nature_2026_BMI_child_adolescent_world.csv", "world", "csv"),
    ],
    "urban-rural-bmi": [
        ("bmi-2019/NCD_RisC_Nature_2019_age_standardised_country.csv", "country", "csv"),
        ("bmi-2019/NCD_RisC_Nature_2019_age_standardised_region.csv", "region", "csv"),
        ("bmi-2019/NCD_RisC_Nature_2019_age_standardised_world.csv", "world", "csv"),
    ],
    "diabetes": [
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_countries.csv", "country", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_regions.csv", "region", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_world.csv", "world", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_countries.csv", "country", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_regions.csv", "region", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_world.csv", "world", "csv"),
    ],
    "cholesterol": [
        ("chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_countries.csv", "country", "csv"),
        ("chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_regions.csv", "region", "csv"),
        ("chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_world.csv", "world", "csv"),
    ],
    "blood-pressure": [
        ("bp/NCD_RisC_Lancet_2017_BP_age_standardised_countries.csv", "country", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_age_standardised_regions.csv", "region", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_age_standardised_world.csv", "world", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_crude_countries.csv", "country", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_crude_regions.csv", "region", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_crude_world.csv", "world", "csv"),
    ],
    "hypertension": [
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_countries.csv", "country", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_regions.csv", "region", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_world.csv", "world", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_countries.csv", "country", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_regions.csv", "region", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_world.csv", "world", "csv"),
    ],
    "child-adolescent-height": [
        ("bmi-height-2020/height/global/NCD_RisC_Lancet_2020_height_child_adolescent_global.csv", "world", "csv"),
        ("bmi-height-2020/height/regional/NCD_RisC_Lancet_2020_height_child_adolescent_region.csv", "region", "csv"),
        ("bmi-height-2020/height/all_countries/NCD_RisC_Lancet_2020_height_child_adolescent_country.zip", "country", "zip"),
    ],
}

LOWER_SUFFIX = " lower 95% uncertainty interval"
UPPER_SUFFIX = " upper 95% uncertainty interval"
# Column names (after strip) treated as dimensions, never as indicators.
DIM_NAMES = {"Country/Region/World", "ISO", "Sex", "Year", "Age", "Age group"}


@transient_retry(attempts=6, min_wait=4, max_wait=120)
def _download(url: str) -> bytes:
    # Generous read timeout: the source serves some multi-MB files slowly.
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _parse_csv_bytes(content: bytes, level: str) -> pd.DataFrame:
    """Unpivot one wide NCD-RisC CSV into the uniform tidy long schema."""
    df = pd.read_csv(io.BytesIO(content), dtype=str, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    cols = list(df.columns)

    # The unit may trail the suffix, e.g. "Mean X lower 95% ... (mmol/L)" -> base
    # "Mean X (mmol/L)". Reconstruct the base by removing the suffix substring.
    lowers = {c.replace(LOWER_SUFFIX, ""): c for c in cols if LOWER_SUFFIX in c}
    uppers = {c.replace(UPPER_SUFFIX, ""): c for c in cols if UPPER_SUFFIX in c}
    bases = [c for c in cols if c in lowers and c in uppers]
    if not bases:
        raise ValueError(f"no indicator triples found; columns={cols[:8]}")

    entity_col = "Country/Region/World" if "Country/Region/World" in cols else None
    iso_col = "ISO" if "ISO" in cols else None
    sex_col = "Sex" if "Sex" in cols else None
    year_col = "Year" if "Year" in cols else None
    age_col = "Age" if "Age" in cols else ("Age group" if "Age group" in cols else None)

    n = len(df)
    entity = df[entity_col] if entity_col else pd.Series(["World"] * n)
    iso = df[iso_col] if iso_col else pd.Series([None] * n)
    sex = df[sex_col] if sex_col else pd.Series([None] * n)
    year = df[year_col] if year_col else pd.Series([None] * n)
    age = df[age_col] if age_col else pd.Series([None] * n)

    frames = []
    for base in bases:
        frames.append(pd.DataFrame({
            "entity": entity.values,
            "iso": iso.values,
            "sex": sex.values,
            "year": year.values,
            "age": age.values,
            "geographic_level": level,
            "indicator": base,
            "value": df[base].values,
            "lower_95": df[lowers[base]].values,
            "upper_95": df[uppers[base]].values,
        }))
    return pd.concat(frames, ignore_index=True)


def _to_table(long: pd.DataFrame) -> pa.Table:
    for c in ("value", "lower_95", "upper_95"):
        long[c] = pd.to_numeric(long[c], errors="coerce")
    long["year"] = pd.to_numeric(long["year"], errors="coerce")
    # Drop rows with no central estimate or no year (nothing to publish).
    long = long.dropna(subset=["value", "year"])
    long["year"] = long["year"].astype("int64")
    for c in ("entity", "iso", "sex", "age", "indicator"):
        long[c] = long[c].where(long[c].notna(), None)
    return pa.Table.from_pandas(long[SCHEMA.names], schema=SCHEMA, preserve_index=False)


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = node_id[len(PREFIX):]
    specs = FILES[entity_id]

    frames = []
    for path, level, kind in specs:
        url = f"{BASE}/{path}"
        try:
            content = _download(url)
        except httpx.HTTPStatusError as e:
            if e.response is not None and e.response.status_code == 404:
                print(f"{asset}: {url} -> 404, skipping")
                continue
            raise

        if kind == "zip":
            zf = zipfile.ZipFile(io.BytesIO(content))
            members = [m for m in zf.namelist() if m.lower().endswith(".csv")]
            if not members:
                raise ValueError(f"{url}: zip has no CSV members")
            for m in members:
                with zf.open(m) as f:
                    frames.append(_parse_csv_bytes(f.read(), level))
        else:
            frames.append(_parse_csv_bytes(content, level))

    if not frames:
        raise RuntimeError(f"{asset}: no source files yielded data")

    table = _to_table(pd.concat(frames, ignore_index=True))
    if table.num_rows == 0:
        raise RuntimeError(f"{asset}: 0 rows after parsing")
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in FILES
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                entity,
                iso,
                sex,
                CAST(year AS INTEGER) AS year,
                age,
                geographic_level,
                indicator,
                CAST(value AS DOUBLE)    AS value,
                CAST(lower_95 AS DOUBLE) AS lower_95,
                CAST(upper_95 AS DOUBLE) AS upper_95
            FROM "{s.id}"
            WHERE value IS NOT NULL AND year IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
