"""Maddison Project — regional aggregates.

The 'Regional data' sheet of mpd2023_web.xlsx: a wide layout with two blocks
side by side — GDP-per-capita for 8 world regions + a World column, then a blank
spacer, then Regional Population for the same regions + World. Unpivoted here to
a tidy (region, year, gdppc, pop) long table.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet
from utils import load_workbook, to_float, to_int

REGIONAL_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("year", pa.int64()),
    ("gdppc", pa.float64()),
    ("pop", pa.float64()),
])


def fetch_regional_aggregates(node_id: str) -> None:
    """The 'Regional data' sheet: a wide layout with two blocks side by side —
    GDP-per-capita for 8 world regions + a World column (cols 1..9), then a blank
    spacer, then Regional Population for the same 8 regions + World (cols 11..19).
    Year is col 0. Unpivot both blocks into a tidy (region, year, gdppc, pop)
    long table, aligning the population columns to the GDPpc region names by
    position (the sheet repeats the same region order)."""
    asset = node_id
    wb = load_workbook()
    ws = wb["Regional data"]
    grid = list(ws.iter_rows(values_only=True))
    wb.close()

    # Row index 1 holds the region labels for the GDPpc block (cols 1..8);
    # col 9 is World GDPpc, cols 11..18 mirror the regions for Population,
    # col 19 is World Population. Data rows start at index 2.
    label_row = grid[1]
    region_names = [str(label_row[c]).strip() for c in range(1, 9)]
    assert len(region_names) == 8 and all(region_names), \
        f"Regional data region labels drift: {region_names!r}"
    # (region_name, gdppc_col, pop_col)
    columns = [(region_names[i], 1 + i, 11 + i) for i in range(8)]
    columns.append(("World", 9, 19))

    rows = []
    for r in grid[2:]:
        year = to_int(r[0])
        if year is None:
            continue
        for region, gcol, pcol in columns:
            gdppc = to_float(r[gcol]) if gcol < len(r) else None
            pop = to_float(r[pcol]) if pcol < len(r) else None
            if gdppc is None and pop is None:
                continue
            rows.append({
                "region": region,
                "year": year,
                "gdppc": gdppc,
                "pop": pop,
            })
    assert rows, "Regional data sheet produced no rows"
    table = pa.Table.from_pylist(rows, schema=REGIONAL_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="maddison-project-regional-aggregates", fn=fetch_regional_aggregates, kind="download"),
]
