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
import re
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
    ("age_group", pa.string()),         # real age range (e.g. "20-24"), null when aggregated
    ("estimate_type", pa.string()),     # age_standardised | crude | age_specific
    ("geographic_level", pa.string()),  # country | region | world
    ("indicator", pa.string()),         # central-estimate column name (incl. unit)
    ("value", pa.float64()),
    ("lower_95", pa.float64()),
    ("upper_95", pa.float64()),
])

# Per risk factor: the source files to union. Each is (path, level, estimate_type, kind).
#   level         : country | region | world
#   estimate_type : how the estimate is aggregated over age, taken from the filename
#                   (age_standardised | crude | age_specific). NOT all releases carry
#                   an "Age" column, so this disambiguates age-std vs crude rows.
#   kind          : "csv" = a direct CSV; "zip" = a zip archive of per-country CSVs.
# Filenames verified from the ncdrisc.org data-download pages.
FILES = {
    "adult-bmi": [
        ("bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_country.csv", "country", "age_standardised", "csv"),
        ("bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_region.csv", "region", "age_standardised", "csv"),
        ("bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_world.csv", "world", "age_standardised", "csv"),
    ],
    "child-adolescent-bmi": [
        ("bmi-2026/child_ado/NCD_RisC_Nature_2026_BMI_child_adolescent_country_ageStd.csv", "country", "age_standardised", "csv"),
        ("bmi-2026/child_ado/NCD_RisC_Nature_2026_BMI_child_adolescent_region.csv", "region", "age_specific", "csv"),
        ("bmi-2026/child_ado/NCD_RisC_Nature_2026_BMI_child_adolescent_world.csv", "world", "age_specific", "csv"),
    ],
    "urban-rural-bmi": [
        ("bmi-2019/NCD_RisC_Nature_2019_age_standardised_country.csv", "country", "age_standardised", "csv"),
        ("bmi-2019/NCD_RisC_Nature_2019_age_standardised_region.csv", "region", "age_standardised", "csv"),
        ("bmi-2019/NCD_RisC_Nature_2019_age_standardised_world.csv", "world", "age_standardised", "csv"),
    ],
    "diabetes": [
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_countries.csv", "country", "age_standardised", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_regions.csv", "region", "age_standardised", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_world.csv", "world", "age_standardised", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_countries.csv", "country", "crude", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_regions.csv", "region", "crude", "csv"),
        ("dm-2024/NCD_RisC_Lancet_2024_Diabetes_crude_world.csv", "world", "crude", "csv"),
    ],
    "cholesterol": [
        ("chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_countries.csv", "country", "age_standardised", "csv"),
        ("chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_regions.csv", "region", "age_standardised", "csv"),
        ("chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_world.csv", "world", "age_standardised", "csv"),
    ],
    "blood-pressure": [
        ("bp/NCD_RisC_Lancet_2017_BP_age_standardised_countries.csv", "country", "age_standardised", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_age_standardised_regions.csv", "region", "age_standardised", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_age_standardised_world.csv", "world", "age_standardised", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_crude_countries.csv", "country", "crude", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_crude_regions.csv", "region", "crude", "csv"),
        ("bp/NCD_RisC_Lancet_2017_BP_crude_world.csv", "world", "crude", "csv"),
    ],
    "hypertension": [
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_countries.csv", "country", "age_standardised", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_regions.csv", "region", "age_standardised", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_world.csv", "world", "age_standardised", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_countries.csv", "country", "crude", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_regions.csv", "region", "crude", "csv"),
        ("hypertension/NCD-RisC_Lancet_2021_Hypertension_crude_world.csv", "world", "crude", "csv"),
    ],
    "child-adolescent-height": [
        ("bmi-height-2020/height/global/NCD_RisC_Lancet_2020_height_child_adolescent_global.csv", "world", "age_specific", "csv"),
        ("bmi-height-2020/height/regional/NCD_RisC_Lancet_2020_height_child_adolescent_region.csv", "region", "age_specific", "csv"),
        ("bmi-height-2020/height/all_countries/NCD_RisC_Lancet_2020_height_child_adolescent_country.zip", "country", "age_specific", "zip"),
    ],
}

# Bound columns are named one of two ways across releases:
#   prefixed:   "<indicator> lower 95% uncertainty interval [(unit)]"  (most files)
#   standalone: "Lower 95% uncertainty interval"  (single-indicator files, e.g. BP)
# Match case-insensitively and reconstruct the base indicator by removing the phrase.
LOWER_RE = re.compile(r"lower 95% uncertainty interval", re.I)
UPPER_RE = re.compile(r"upper 95% uncertainty interval", re.I)
# Column names treated as dimensions, never as indicators.
DIM_NAMES = {"Country/Region/World", "ISO", "Sex", "Year", "Age", "Age group"}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


@transient_retry(attempts=6, min_wait=4, max_wait=120)
def _download(url: str) -> bytes:
    # Generous read timeout: the source serves some multi-MB files slowly.
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _find_triples(cols: list) -> list:
    """Pair each central indicator column with its lower/upper 95% bound columns.

    Returns a list of (central_col, lower_col, upper_col). Handles both
    prefixed bounds (matched by base name) and a single standalone generic
    bound pair (matched to the lone unpaired indicator).
    """
    lower_cols = [c for c in cols if LOWER_RE.search(c)]
    upper_cols = [c for c in cols if UPPER_RE.search(c)]
    bound_set = set(lower_cols) | set(upper_cols)
    centrals = [c for c in cols if c not in bound_set and c not in DIM_NAMES]

    lower_by_base = {_norm(LOWER_RE.sub(" ", c)): c for c in lower_cols}
    upper_by_base = {_norm(UPPER_RE.sub(" ", c)): c for c in upper_cols}

    triples, unpaired = [], []
    for c in centrals:
        k = _norm(c)
        lc, uc = lower_by_base.get(k), upper_by_base.get(k)
        if lc and uc:
            triples.append((c, lc, uc))
        else:
            unpaired.append(c)

    # Standalone generic bounds (base "") attach to the single unpaired indicator.
    gl, gu = lower_by_base.get(""), upper_by_base.get("")
    if len(unpaired) == 1 and gl and gu:
        triples.append((unpaired[0], gl, gu))
        unpaired = []

    if not triples:
        raise ValueError(f"no indicator triples found; columns={cols[:10]}")
    if unpaired:
        # Columns without a 95% bound pair are ancillary stats (e.g. "Mean height
        # standard error"), not publishable indicators. Drop them, but log so a
        # genuinely new bound-less indicator doesn't vanish silently.
        print(f"ignoring non-indicator columns (no 95% bounds): {unpaired}")
    return triples


# "Age"-column values that are really an aggregation label, not a real age range.
_AGG_LABELS = {"age-standardised", "age-standardized", "crude", "total", "all ages"}


def _parse_csv_bytes(content: bytes, level: str, estimate_type: str) -> pd.DataFrame:
    """Unpivot one wide NCD-RisC CSV into the uniform tidy long schema."""
    df = pd.read_csv(io.BytesIO(content), dtype=str, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    cols = list(df.columns)
    triples = _find_triples(cols)

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
    # age_group holds only real age ranges; aggregation labels ("Age-standardised",
    # "Crude") are dropped because estimate_type already captures them.
    if age_col:
        age_raw = df[age_col]
        is_label = age_raw.astype(str).str.strip().str.lower().isin(_AGG_LABELS)
        age_group = age_raw.mask(is_label, other=None)
    else:
        age_group = pd.Series([None] * n)

    frames = []
    for central, lc, uc in triples:
        frames.append(pd.DataFrame({
            "entity": entity.values,
            "iso": iso.values,
            "sex": sex.values,
            "year": year.values,
            "age_group": age_group.values,
            "estimate_type": estimate_type,
            "geographic_level": level,
            "indicator": _norm(central),
            "value": df[central].values,
            "lower_95": df[lc].values,
            "upper_95": df[uc].values,
        }))
    return pd.concat(frames, ignore_index=True)


def _to_table(long: pd.DataFrame) -> pa.Table:
    for c in ("value", "lower_95", "upper_95"):
        long[c] = pd.to_numeric(long[c], errors="coerce")
    long["year"] = pd.to_numeric(long["year"], errors="coerce")
    # Drop rows with no central estimate or no year (nothing to publish).
    long = long.dropna(subset=["value", "year"])
    long["year"] = long["year"].astype("int64")
    for c in ("entity", "iso", "sex", "age_group", "indicator"):
        long[c] = long[c].where(long[c].notna(), None)
    return pa.Table.from_pandas(long[SCHEMA.names], schema=SCHEMA, preserve_index=False)


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = node_id[len(PREFIX):]
    specs = FILES[entity_id]

    frames = []
    for path, level, estimate_type, kind in specs:
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
                    frames.append(_parse_csv_bytes(f.read(), level, estimate_type))
        else:
            frames.append(_parse_csv_bytes(content, level, estimate_type))

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
                age_group,
                estimate_type,
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
