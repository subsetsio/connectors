"""JMD age-by-year measures — one parametric family.

Four published subsets share the exact same file shape ('Year Age female male
total') and schema, differing only in the source filename; one parametric
fetcher (`_save_age_measure`) drives all of them:

  jmd-deaths       death counts        (Deaths_1x1.txt)
  jmd-population   population sizes     (Population.txt)
  jmd-exposures    exposure-to-risk    (Exposures_1x1.txt)
  jmd-death-rates  central death rates (Mx_1x1.txt)

Area is a *column*, not a separate subset.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _data_lines, _iter_areas, _num, _year


def _save_age_measure(node_id: str, filename: str, value_cols):
    """Files shaped 'Year Age <value_cols...>' (Deaths/Population/Exposures/Mx).
    value_cols is the list of output column names for the trailing numerics."""
    cols = {k: [] for k in ("area", "area_name", "year", "age", *value_cols)}
    ncols = 2 + len(value_cols)
    for code, name, text in _iter_areas(filename):
        for line in _data_lines(text):
            tok = line.split()
            if len(tok) < ncols:
                continue
            yr = _year(tok[0])
            if yr is None:
                continue
            cols["area"].append(code)
            cols["area_name"].append(name)
            cols["year"].append(yr)
            cols["age"].append(tok[1])
            for i, vc in enumerate(value_cols):
                cols[vc].append(_num(tok[2 + i]))

    schema = pa.schema(
        [("area", pa.string()), ("area_name", pa.string()),
         ("year", pa.int32()), ("age", pa.string())]
        + [(vc, pa.float64()) for vc in value_cols]
    )
    table = pa.table({k: cols[k] for k in schema.names}, schema=schema)
    save_raw_parquet(table, node_id)


def fetch_deaths(node_id: str) -> None:
    _save_age_measure(node_id, "Deaths_1x1.txt", ["female", "male", "total"])


def fetch_population(node_id: str) -> None:
    _save_age_measure(node_id, "Population.txt", ["female", "male", "total"])


def fetch_exposures(node_id: str) -> None:
    _save_age_measure(node_id, "Exposures_1x1.txt", ["female", "male", "total"])


def fetch_death_rates(node_id: str) -> None:
    _save_age_measure(node_id, "Mx_1x1.txt", ["female", "male", "total"])


_FETCH = {
    "ipss-japan-jmd-deaths": fetch_deaths,
    "ipss-japan-jmd-population": fetch_population,
    "ipss-japan-jmd-exposures": fetch_exposures,
    "ipss-japan-jmd-death-rates": fetch_death_rates,
}

DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fn, kind="download") for sid, fn in _FETCH.items()
]


def _t(download_id: str) -> str:
    return f"{download_id}-transform"


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=_t("ipss-japan-jmd-deaths"),
        deps=["ipss-japan-jmd-deaths"],
        sql='''
            SELECT area, area_name, CAST(year AS INTEGER) AS year, age,
                   female, male, total
            FROM "ipss-japan-jmd-deaths"
            WHERE year IS NOT NULL AND age IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=_t("ipss-japan-jmd-population"),
        deps=["ipss-japan-jmd-population"],
        sql='''
            SELECT area, area_name, CAST(year AS INTEGER) AS year, age,
                   female, male, total
            FROM "ipss-japan-jmd-population"
            WHERE year IS NOT NULL AND age IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=_t("ipss-japan-jmd-exposures"),
        deps=["ipss-japan-jmd-exposures"],
        sql='''
            SELECT area, area_name, CAST(year AS INTEGER) AS year, age,
                   female, male, total
            FROM "ipss-japan-jmd-exposures"
            WHERE year IS NOT NULL AND age IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=_t("ipss-japan-jmd-death-rates"),
        deps=["ipss-japan-jmd-death-rates"],
        sql='''
            SELECT area, area_name, CAST(year AS INTEGER) AS year, age,
                   female, male, total
            FROM "ipss-japan-jmd-death-rates"
            WHERE year IS NOT NULL AND age IS NOT NULL
        ''',
    ),
]
