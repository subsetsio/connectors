"""Fórum Brasileiro de Segurança Pública — Anuário data tables.

One download node per rank-accepted table in the latest *Anuário Brasileiro de
Segurança Pública* workbook (published in the FBSP DSpace repository as a single
multi-sheet xlsx). Every accepted table is a Brazilian-state (UF) by year
cross-tab of public-security statistics — homicides, police lethality, sexual
and domestic violence, firearms, drugs, public-security spending, the prison
system and juvenile justice.

Each fetch resolves the newest edition via the DSpace discover API (so the
connector tracks new editions automatically — no hard-coded UUIDs), downloads
the workbook, matches the entity to its current sheet by title slug, and parses
that sheet into a tidy long table (geography, geo_level, year, measure, value).
Stateless full re-pull: the corpus is one ~2 MB workbook, so every run re-reads
the latest edition and overwrites. The transform is a thin cast/projection.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet

from constants import ENTITY_IDS
from utils import fetch_workbook, index_slug_to_code, parse_table

SLUG = "forum-brasileiro-seguranca"

SCHEMA = pa.schema([
    ("geography", pa.string()),   # Brasil / region / state label, verbatim
    ("geo_level", pa.string()),   # 'brasil' | 'regiao' | 'uf'
    ("year", pa.int64()),
    ("measure", pa.string()),     # metric / breakdown label above the year column
    ("value", pa.float64()),
])


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_key = node_id[len(SLUG) + 1:]  # strip "forum-brasileiro-seguranca-"

    xlsx = fetch_workbook()
    code = index_slug_to_code(xlsx).get(entity_key)
    if code is None:
        raise RuntimeError(
            f"{entity_key}: no matching table in the latest Anuário Índice "
            "(title may have changed between editions)"
        )

    rows = parse_table(xlsx, code)
    if not rows:
        raise RuntimeError(f"{entity_key}: sheet {code} parsed to 0 rows")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
