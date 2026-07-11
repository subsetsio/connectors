"""ITU DataHub - thematic indicator taxonomy."""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _as_int, _get_json

_CATEGORIES_SCHEMA = pa.schema([
    ("category", pa.string()),
    ("category_sort", pa.int64()),
    ("sub_category", pa.string()),
    ("sub_category_sort", pa.int64()),
    ("code_id", pa.int64()),
    ("label", pa.string()),
    ("database_id", pa.int64()),
    ("series_type", pa.string()),
    ("indicator_sort", pa.int64()),
    ("external", pa.bool_()),
    ("is_collection", pa.bool_()),
])


def fetch_categories(node_id: str) -> None:
    rows = _get_json("dictionaries/getcategories")
    cols = {k: [] for k in _CATEGORIES_SCHEMA.names}

    for category in rows:
        category_name = category.get("category")
        category_sort = _as_int(category.get("categorySort"))
        for sub_category in category.get("subCategory", []):
            sub_name = sub_category.get("subCategory")
            sub_sort = _as_int(sub_category.get("subCategorySort"))
            items = sub_category.get("items") or []
            if not items:
                cols["category"].append(category_name)
                cols["category_sort"].append(category_sort)
                cols["sub_category"].append(sub_name)
                cols["sub_category_sort"].append(sub_sort)
                cols["code_id"].append(None)
                cols["label"].append(None)
                cols["database_id"].append(None)
                cols["series_type"].append(None)
                cols["indicator_sort"].append(None)
                cols["external"].append(None)
                cols["is_collection"].append(None)
                continue

            for item in items:
                cols["category"].append(category_name)
                cols["category_sort"].append(category_sort)
                cols["sub_category"].append(sub_name)
                cols["sub_category_sort"].append(sub_sort)
                cols["code_id"].append(_as_int(item.get("codeID")))
                cols["label"].append(item.get("label"))
                cols["database_id"].append(_as_int(item.get("databaseID")))
                cols["series_type"].append(item.get("seriesType"))
                cols["indicator_sort"].append(_as_int(item.get("indicatorSort")))
                cols["external"].append(item.get("external"))
                cols["is_collection"].append(item.get("isCollection"))

    table = pa.table(cols, schema=_CATEGORIES_SCHEMA)
    save_raw_parquet(table, node_id)
