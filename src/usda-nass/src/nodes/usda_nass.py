"""USDA NASS Quick Stats — agricultural statistics, one long-format table per commodity.

Source: the full Quick Stats database, published as 5 gzipped tab-delimited
sector dumps at https://www.nass.usda.gov/datasets/ (no API key needed; the
REST API is key-gated and the deployment has no such secret — see research).

Architecture (one bulk source fanning out to 210 commodity subsets):
  * A single LOADER download (id "usda-nass-ag-land") fetches all 5 sector
    files ONCE, splits each by COMMODITY_DESC into a local Hive-partitioned
    parquet cache, then streams one raw parquet asset per accepted commodity
    (memory-bounded via raw_parquet_writer). The split happens exactly once.
  * Every other commodity download depends on the loader and simply verifies
    its raw asset landed — re-fetching a 1 GB bulk file per commodity would be
    absurd, and the harness requires one download spec per entity.
  * One SQL transform per commodity cleans/casts its slice into a tidy
    long-format table (year x location x series), mapping USDA suppression
    codes ((D)/(Z)/(NA)/...) and blanks to NULL.
"""
import os
import re
import shutil
import tempfile

import duckdb

from subsets_utils import (
    NodeSpec, SqlNodeSpec,
    get_client, raw_parquet_writer, raw_asset_exists,
)
from subsets_utils.duckdb import _configure

INDEX_URL = "https://www.nass.usda.gov/datasets/"
SECTOR_TOKENS = ("animals_products", "crops", "demographics", "economics", "environmental")

# Columns pulled from the raw TSV (subset of the ~40 NASS columns). COMMODITY_DESC
# is the partition key (removed from each file, restored on read via hive partitioning).
SELECT_COLS = (
    "SOURCE_DESC", "SECTOR_DESC", "GROUP_DESC", "COMMODITY_DESC", "CLASS_DESC",
    "PRODN_PRACTICE_DESC", "UTIL_PRACTICE_DESC", "STATISTICCAT_DESC", "UNIT_DESC",
    "SHORT_DESC", "DOMAIN_DESC", "DOMAINCAT_DESC", "AGG_LEVEL_DESC",
    "STATE_ALPHA", "STATE_NAME", "ASD_DESC", "COUNTY_NAME", "REGION_DESC",
    "LOCATION_DESC", "YEAR", "FREQ_DESC", "REFERENCE_PERIOD_DESC", "WEEK_ENDING",
    "VALUE", "CV_%",
)

LOADER_ID = "ag-land"

# entity_id -> (COMMODITY_DESC, (sector_token, ...)) for every rank-accepted commodity.
ENTITY_META = {
    'ag-land': ('AG LAND', ('demographics', 'economics', 'environmental')),
    'ag-services': ('AG SERVICES', ('demographics', 'economics')),
    'almonds': ('ALMONDS', ('crops', 'demographics', 'environmental')),
    'animal-totals': ('ANIMAL TOTALS', ('animals_products', 'demographics', 'economics')),
    'apples': ('APPLES', ('crops', 'demographics', 'environmental')),
    'apricots': ('APRICOTS', ('crops', 'demographics', 'environmental')),
    'artichokes': ('ARTICHOKES', ('crops', 'demographics', 'environmental')),
    'asparagus': ('ASPARAGUS', ('crops', 'demographics', 'environmental')),
    'avocados': ('AVOCADOS', ('crops', 'demographics', 'environmental')),
    'barley': ('BARLEY', ('crops', 'demographics', 'environmental')),
    'beans': ('BEANS', ('crops', 'demographics', 'environmental')),
    'bedding-plant-totals': ('BEDDING PLANT TOTALS', ('crops', 'demographics')),
    'bedding-plants-annual': ('BEDDING PLANTS, ANNUAL', ('crops', 'environmental')),
    'bedding-plants-herbaceous-perennial': ('BEDDING PLANTS, HERBACEOUS PERENNIAL', ('crops', 'environmental')),
    'beef': ('BEEF', ('animals_products',)),
    'beets': ('BEETS', ('crops', 'demographics', 'environmental')),
    'berries-other': ('BERRIES, OTHER', ('crops', 'environmental')),
    'bison': ('BISON', ('animals_products', 'demographics')),
    'blackberries': ('BLACKBERRIES', ('crops', 'demographics', 'environmental')),
    'blueberries': ('BLUEBERRIES', ('crops', 'demographics', 'environmental')),
    'boysenberries': ('BOYSENBERRIES', ('crops',)),
    'broccoli': ('BROCCOLI', ('crops', 'demographics', 'environmental')),
    'brussels-sprouts': ('BRUSSELS SPROUTS', ('crops', 'demographics', 'environmental')),
    'building-materials': ('BUILDING MATERIALS', ('economics',)),
    'butter': ('BUTTER', ('animals_products',)),
    'buttermilk': ('BUTTERMILK', ('animals_products',)),
    'cabbage': ('CABBAGE', ('crops', 'demographics', 'environmental')),
    'canola': ('CANOLA', ('crops', 'demographics')),
    'carrots': ('CARROTS', ('crops', 'demographics', 'environmental')),
    'cattle': ('CATTLE', ('animals_products', 'demographics', 'economics')),
    'cauliflower': ('CAULIFLOWER', ('crops', 'demographics', 'environmental')),
    'celery': ('CELERY', ('crops', 'demographics', 'environmental')),
    'cheese': ('CHEESE', ('animals_products',)),
    'chemical-totals': ('CHEMICAL TOTALS', ('demographics', 'economics')),
    'cherries': ('CHERRIES', ('crops', 'demographics', 'environmental')),
    'chickens': ('CHICKENS', ('animals_products', 'demographics')),
    'chickpeas': ('CHICKPEAS', ('crops', 'demographics')),
    'citrus-totals': ('CITRUS TOTALS', ('crops', 'demographics')),
    'coffee': ('COFFEE', ('crops', 'demographics')),
    'commodity-totals': ('COMMODITY TOTALS', ('demographics', 'economics')),
    'corn': ('CORN', ('crops', 'demographics', 'environmental')),
    'cotton': ('COTTON', ('crops', 'demographics', 'environmental')),
    'cranberries': ('CRANBERRIES', ('crops', 'demographics', 'environmental')),
    'crop-totals': ('CROP TOTALS', ('crops', 'demographics', 'economics', 'environmental')),
    'crops-other': ('CROPS, OTHER', ('crops', 'environmental')),
    'cucumbers': ('CUCUMBERS', ('crops', 'demographics', 'environmental')),
    'cut-christmas-trees': ('CUT CHRISTMAS TREES', ('crops', 'demographics', 'environmental')),
    'cut-cultivated-greens': ('CUT CULTIVATED GREENS', ('crops', 'environmental')),
    'cut-flowers': ('CUT FLOWERS', ('crops', 'environmental')),
    'dairy-product-totals': ('DAIRY PRODUCT TOTALS', ('animals_products',)),
    'dairy-products-other': ('DAIRY PRODUCTS, OTHER', ('animals_products',)),
    'dates': ('DATES', ('crops', 'demographics', 'environmental')),
    'deciduous-flowering-trees': ('DECIDUOUS FLOWERING TREES', ('crops', 'environmental')),
    'deciduous-shade-trees': ('DECIDUOUS SHADE TREES', ('crops', 'environmental')),
    'deciduous-shrubs': ('DECIDUOUS SHRUBS', ('crops', 'environmental')),
    'ducks': ('DUCKS', ('animals_products', 'demographics')),
    'eggplant': ('EGGPLANT', ('crops', 'demographics', 'environmental')),
    'eggs': ('EGGS', ('animals_products', 'demographics')),
    'equine': ('EQUINE', ('animals_products', 'demographics')),
    'escarole-endive': ('ESCAROLE & ENDIVE', ('crops',)),
    'evergreens-broadleaf': ('EVERGREENS, BROADLEAF', ('crops', 'environmental')),
    'evergreens-coniferous': ('EVERGREENS, CONIFEROUS', ('crops', 'environmental')),
    'expense-totals': ('EXPENSE TOTALS', ('demographics', 'economics')),
    'farm-operations': ('FARM OPERATIONS', ('demographics', 'economics')),
    'feed': ('FEED', ('animals_products', 'demographics', 'economics')),
    'fertilizer-mixed': ('FERTILIZER, MIXED', ('economics',)),
    'fertilizer-totals': ('FERTILIZER TOTALS', ('demographics', 'economics')),
    'field-crop-totals': ('FIELD CROP TOTALS', ('crops', 'demographics', 'economics')),
    'field-crops-other': ('FIELD CROPS, OTHER', ('crops', 'demographics', 'environmental')),
    'fieldwork': ('FIELDWORK', ('crops',)),
    'figs': ('FIGS', ('crops', 'demographics', 'environmental')),
    'flaxseed': ('FLAXSEED', ('crops', 'demographics')),
    'floriculture-totals': ('FLORICULTURE TOTALS', ('crops', 'demographics', 'environmental')),
    'flowering-plants-potted': ('FLOWERING PLANTS, POTTED', ('crops', 'demographics', 'environmental')),
    'foliage-plants': ('FOLIAGE PLANTS', ('crops', 'demographics', 'environmental')),
    'food-fish': ('FOOD FISH', ('animals_products',)),
    'food-grains': ('FOOD GRAINS', ('crops',)),
    'fruit-nut-plants': ('FRUIT & NUT PLANTS', ('crops', 'environmental')),
    'fruit-other': ('FRUIT, OTHER', ('crops', 'demographics')),
    'fruit-totals': ('FRUIT TOTALS', ('crops',)),
    'fruit-tree-nut-totals': ('FRUIT & TREE NUT TOTALS', ('crops', 'demographics', 'environmental')),
    'fuels': ('FUELS', ('demographics', 'economics')),
    'garlic': ('GARLIC', ('crops', 'demographics', 'environmental')),
    'goats': ('GOATS', ('animals_products', 'demographics')),
    'grain': ('GRAIN', ('crops', 'demographics', 'environmental')),
    'grain-storage-capacity': ('GRAIN STORAGE CAPACITY', ('crops',)),
    'grapefruit': ('GRAPEFRUIT', ('crops', 'demographics', 'environmental')),
    'grapes': ('GRAPES', ('crops', 'demographics', 'environmental')),
    'grasses': ('GRASSES', ('crops', 'economics')),
    'grasses-legumes-totals': ('GRASSES & LEGUMES TOTALS', ('crops', 'demographics', 'economics')),
    'greens': ('GREENS', ('crops', 'demographics', 'environmental')),
    'hay': ('HAY', ('crops', 'demographics', 'environmental')),
    'hay-haylage': ('HAY & HAYLAGE', ('crops', 'demographics', 'environmental')),
    'haylage': ('HAYLAGE', ('crops',)),
    'hazelnuts': ('HAZELNUTS', ('crops', 'demographics', 'environmental')),
    'hemp': ('HEMP', ('crops', 'demographics')),
    'herbicides': ('HERBICIDES', ('economics',)),
    'hogs': ('HOGS', ('animals_products', 'demographics', 'economics')),
    'honey': ('HONEY', ('animals_products', 'demographics')),
    'hops': ('HOPS', ('crops', 'demographics')),
    'horticulture-totals': ('HORTICULTURE TOTALS', ('crops', 'demographics', 'environmental')),
    'ice-cream': ('ICE CREAM', ('animals_products',)),
    'insecticides': ('INSECTICIDES', ('economics',)),
    'interest': ('INTEREST', ('demographics', 'economics')),
    'internet': ('INTERNET', ('demographics',)),
    'kiwifruit': ('KIWIFRUIT', ('crops', 'demographics', 'environmental')),
    'labor': ('LABOR', ('demographics', 'economics')),
    'lamb-mutton': ('LAMB & MUTTON', ('animals_products',)),
    'legumes': ('LEGUMES', ('crops', 'economics')),
    'lemons': ('LEMONS', ('crops', 'demographics', 'environmental')),
    'lentils': ('LENTILS', ('crops', 'demographics')),
    'lettuce': ('LETTUCE', ('crops', 'demographics', 'environmental')),
    'limes': ('LIMES', ('crops', 'demographics', 'environmental')),
    'livestock-totals': ('LIVESTOCK TOTALS', ('animals_products', 'demographics')),
    'loganberries': ('LOGANBERRIES', ('crops',)),
    'macadamias': ('MACADAMIAS', ('crops', 'demographics')),
    'machinery-other': ('MACHINERY, OTHER', ('demographics', 'economics')),
    'machinery-totals': ('MACHINERY TOTALS', ('demographics', 'economics')),
    'maple-syrup': ('MAPLE SYRUP', ('crops', 'demographics')),
    'melons': ('MELONS', ('crops', 'demographics', 'environmental')),
    'milk': ('MILK', ('animals_products', 'demographics')),
    'millet': ('MILLET', ('crops', 'demographics')),
    'mink': ('MINK', ('animals_products',)),
    'mint': ('MINT', ('crops', 'demographics')),
    'mohair': ('MOHAIR', ('animals_products',)),
    'mushrooms': ('MUSHROOMS', ('crops',)),
    'mustard': ('MUSTARD', ('crops', 'demographics')),
    'nectarines': ('NECTARINES', ('crops', 'demographics', 'environmental')),
    'nitrogen': ('NITROGEN', ('economics',)),
    'non-citrus-totals': ('NON-CITRUS TOTALS', ('crops',)),
    'nursery-totals': ('NURSERY TOTALS', ('crops', 'demographics', 'environmental')),
    'oats': ('OATS', ('crops', 'demographics', 'environmental')),
    'oil-bearing-crops': ('OIL-BEARING CROPS', ('crops',)),
    'okra': ('OKRA', ('crops', 'demographics', 'environmental')),
    'olives': ('OLIVES', ('crops', 'demographics', 'environmental')),
    'onions': ('ONIONS', ('crops', 'demographics', 'environmental')),
    'operators-principal': ('OPERATORS, PRINCIPAL', ('demographics',)),
    'oranges': ('ORANGES', ('crops', 'demographics', 'environmental')),
    'papayas': ('PAPAYAS', ('crops', 'demographics')),
    'pastureland': ('PASTURELAND', ('crops', 'environmental')),
    'peaches': ('PEACHES', ('crops', 'demographics', 'environmental')),
    'peanuts': ('PEANUTS', ('crops', 'demographics', 'environmental')),
    'pears': ('PEARS', ('crops', 'demographics', 'environmental')),
    'peas': ('PEAS', ('crops', 'demographics', 'environmental')),
    'pecans': ('PECANS', ('crops', 'demographics', 'environmental')),
    'peppers': ('PEPPERS', ('crops', 'demographics', 'environmental')),
    'pistachios': ('PISTACHIOS', ('crops', 'demographics', 'environmental')),
    'pitw': ('PITW', ('economics',)),
    'plums': ('PLUMS', ('crops', 'environmental')),
    'plums-prunes': ('PLUMS & PRUNES', ('crops', 'demographics', 'environmental')),
    'popcorn': ('POPCORN', ('crops', 'demographics')),
    'pork': ('PORK', ('animals_products',)),
    'potatoes': ('POTATOES', ('crops', 'demographics', 'environmental')),
    'poultry-other': ('POULTRY, OTHER', ('animals_products', 'demographics')),
    'poultry-totals': ('POULTRY TOTALS', ('animals_products', 'demographics', 'economics')),
    'ppitw': ('PPITW', ('economics',)),
    'practices': ('PRACTICES', ('animals_products', 'demographics', 'economics')),
    'price-index-ratio': ('PRICE INDEX RATIO', ('economics',)),
    'producers': ('PRODUCERS', ('demographics',)),
    'production-items': ('PRODUCTION ITEMS', ('economics',)),
    'propagative-material': ('PROPAGATIVE MATERIAL', ('crops', 'demographics', 'environmental')),
    'prunes': ('PRUNES', ('crops', 'demographics', 'environmental')),
    'pumpkins': ('PUMPKINS', ('crops', 'demographics', 'environmental')),
    'rapeseed': ('RAPESEED', ('crops', 'demographics')),
    'raspberries': ('RASPBERRIES', ('crops', 'demographics', 'environmental')),
    'red-meat': ('RED MEAT', ('animals_products',)),
    'rent': ('RENT', ('demographics', 'economics')),
    'rice': ('RICE', ('crops', 'demographics', 'environmental')),
    'rye': ('RYE', ('crops', 'demographics')),
    'safflower': ('SAFFLOWER', ('crops', 'demographics')),
    'seeds-plants-totals': ('SEEDS & PLANTS TOTALS', ('demographics', 'economics')),
    'self-propelled': ('SELF PROPELLED', ('demographics', 'economics')),
    'sheep': ('SHEEP', ('animals_products', 'demographics', 'environmental')),
    'sherbet': ('SHERBET', ('animals_products',)),
    'soil': ('SOIL', ('crops',)),
    'sorghum': ('SORGHUM', ('crops', 'demographics', 'environmental')),
    'soybeans': ('SOYBEANS', ('crops', 'demographics', 'environmental')),
    'spinach': ('SPINACH', ('crops', 'demographics', 'environmental')),
    'squash': ('SQUASH', ('crops', 'demographics', 'environmental')),
    'strawberries': ('STRAWBERRIES', ('crops', 'demographics', 'environmental')),
    'sugarbeets': ('SUGARBEETS', ('crops', 'demographics', 'environmental')),
    'sugarcane': ('SUGARCANE', ('crops', 'demographics')),
    'sunflower': ('SUNFLOWER', ('crops', 'demographics', 'environmental')),
    'supplies-repairs': ('SUPPLIES & REPAIRS', ('demographics', 'economics')),
    'sweet-corn': ('SWEET CORN', ('crops', 'demographics', 'environmental')),
    'sweet-potatoes': ('SWEET POTATOES', ('crops', 'demographics')),
    'tangelos': ('TANGELOS', ('crops', 'demographics', 'environmental')),
    'tangerines': ('TANGERINES', ('crops', 'demographics', 'environmental')),
    'taro': ('TARO', ('crops', 'demographics')),
    'taxes': ('TAXES', ('demographics', 'economics')),
    'temples': ('TEMPLES', ('crops', 'environmental')),
    'tobacco': ('TOBACCO', ('crops', 'demographics', 'environmental')),
    'tomatoes': ('TOMATOES', ('crops', 'demographics', 'environmental')),
    'tractors': ('TRACTORS', ('demographics', 'economics')),
    'transplants': ('TRANSPLANTS', ('crops', 'demographics', 'environmental')),
    'tree-nut-totals': ('TREE NUT TOTALS', ('crops',)),
    'trucks': ('TRUCKS', ('demographics', 'economics')),
    'trucks-autos': ('TRUCKS & AUTOS', ('demographics', 'economics')),
    'turkeys': ('TURKEYS', ('animals_products', 'demographics')),
    'veal': ('VEAL', ('animals_products',)),
    'vegetable-totals': ('VEGETABLE TOTALS', ('crops', 'demographics', 'environmental')),
    'vegetables-other': ('VEGETABLES, OTHER', ('crops', 'demographics', 'environmental')),
    'walnuts': ('WALNUTS', ('crops', 'demographics', 'environmental')),
    'water': ('WATER', ('animals_products', 'demographics', 'economics')),
    'water-ices': ('WATER ICES', ('animals_products',)),
    'wheat': ('WHEAT', ('crops', 'demographics', 'environmental')),
    'whey': ('WHEY', ('animals_products',)),
    'woody-ornamentals-vines-other': ('WOODY ORNAMENTALS & VINES, OTHER', ('crops', 'environmental')),
    'wool': ('WOOL', ('animals_products',)),
    'yogurt': ('YOGURT', ('animals_products',)),
}

ENTITY_IDS = list(ENTITY_META)


# --------------------------------------------------------------------------- #
# download
# --------------------------------------------------------------------------- #
def _discover_urls() -> dict:
    """Map sector token -> current date-stamped bulk file URL (scraped from the
    directory listing; filenames carry a YYYYMMDD stamp that rotates weekly)."""
    resp = get_client().get(INDEX_URL, timeout=120)
    resp.raise_for_status()
    html = resp.text
    urls = {}
    for name in sorted(set(re.findall(r"qs\.[a-z_]+_\d{8}\.txt\.gz", html))):
        for tok in SECTOR_TOKENS:
            if name.startswith("qs." + tok + "_"):
                urls[tok] = INDEX_URL + name
    missing = [t for t in SECTOR_TOKENS if t not in urls]
    if missing:
        raise RuntimeError(f"bulk files not found for sectors {missing} at {INDEX_URL}")
    return urls


def _stream_download(url: str, dest: str) -> None:
    client = get_client()
    with client.stream("GET", url, timeout=900) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_bytes(chunk_size=8 * 1024 * 1024):
                f.write(chunk)


def _quoted_cols() -> str:
    return ", ".join('"' + c + '"' for c in SELECT_COLS)


def load_quickstats(spec_id: str) -> None:
    """LOADER: download all 5 sector dumps, partition each by commodity, and
    write one raw parquet asset per accepted commodity. Runs once; every other
    commodity download depends on this node."""
    _configure()
    base = tempfile.mkdtemp(prefix="nass_load_")
    part_root = os.path.join(base, "part")
    os.makedirs(part_root, exist_ok=True)
    try:
        con = duckdb.connect()
        con.execute("SET temp_directory='" + base + "/duckdb_tmp'")
        con.execute("SET preserve_insertion_order=false")
        urls = _discover_urls()
        cols = _quoted_cols()
        for tok in SECTOR_TOKENS:
            gz = os.path.join(base, tok + ".txt.gz")
            print(f"[loader] downloading {urls[tok]}")
            _stream_download(urls[tok], gz)
            out = os.path.join(part_root, tok)
            print(f"[loader] partitioning {tok} by commodity")
            con.execute(
                "COPY (SELECT " + cols + " FROM read_csv('" + gz + "', delim='\t', "
                "header=true, all_varchar=true, quote='', escape='', "
                "encoding='latin-1', strict_mode=false)) "
                "TO '" + out + "' (FORMAT PARQUET, PARTITION_BY (COMMODITY_DESC), "
                "OVERWRITE_OR_IGNORE)"
            )
            os.remove(gz)

        for cid, (commodity, toks) in ENTITY_META.items():
            globs = "[" + ", ".join(
                "'" + part_root + "/" + t + "/**/*.parquet'" for t in toks
            ) + "]"
            esc = commodity.replace("'", "''")
            reader = con.execute(
                "SELECT * FROM read_parquet(" + globs + ", hive_partitioning=true, "
                "union_by_name=true) WHERE COMMODITY_DESC = '" + esc + "'"
            ).fetch_record_batch()
            asset = "usda-nass-" + cid
            with raw_parquet_writer(asset, reader.schema) as w:
                for batch in reader:
                    if batch.num_rows:
                        w.write_batch(batch)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def fetch_commodity(spec_id: str) -> None:
    """Non-loader commodity download: its raw asset is materialized by the
    loader (a declared dependency). Verify it landed rather than re-downloading
    the multi-GB bulk files."""
    if not raw_asset_exists(spec_id, "parquet"):
        raise RuntimeError(
            spec_id + ": raw asset missing — loader 'usda-nass-" + LOADER_ID
            + "' must run first (it is a declared dependency of this node)"
        )


# --------------------------------------------------------------------------- #
# transform
# --------------------------------------------------------------------------- #
def _clean_sql(view: str) -> str:
    return (
        'SELECT '
        'COMMODITY_DESC AS commodity, '
        'SECTOR_DESC AS sector, '
        'GROUP_DESC AS commodity_group, '
        'SOURCE_DESC AS source, '
        'STATISTICCAT_DESC AS statistic, '
        'SHORT_DESC AS series, '
        'UNIT_DESC AS unit, '
        'CLASS_DESC AS class, '
        'PRODN_PRACTICE_DESC AS production_practice, '
        'UTIL_PRACTICE_DESC AS utilization_practice, '
        'DOMAIN_DESC AS domain, '
        'DOMAINCAT_DESC AS domain_category, '
        'AGG_LEVEL_DESC AS agg_level, '
        'STATE_ALPHA AS state_code, '
        'STATE_NAME AS state, '
        'ASD_DESC AS agricultural_district, '
        'COUNTY_NAME AS county, '
        'REGION_DESC AS region, '
        'LOCATION_DESC AS location, '
        'TRY_CAST("YEAR" AS INTEGER) AS year, '
        'FREQ_DESC AS frequency, '
        'REFERENCE_PERIOD_DESC AS reference_period, '
        "NULLIF(TRIM(WEEK_ENDING), '') AS week_ending, "
        "TRY_CAST(REPLACE(TRIM(VALUE), ',', '') AS DOUBLE) AS value, "
        "TRY_CAST(REPLACE(TRIM(\"CV_%\"), ',', '') AS DOUBLE) AS cv_percent "
        'FROM "' + view + '"'
    )


DOWNLOAD_SPECS = [
    NodeSpec(
        id="usda-nass-" + cid,
        fn=load_quickstats if cid == LOADER_ID else fetch_commodity,
        kind="download",
        deps=() if cid == LOADER_ID else ("usda-nass-" + LOADER_ID,),
    )
    for cid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="usda-nass-" + cid + "-transform",
        sql=_clean_sql("usda-nass-" + cid),
        deps=("usda-nass-" + cid,),
    )
    for cid in ENTITY_IDS
]
