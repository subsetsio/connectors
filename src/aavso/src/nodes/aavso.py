"""AAVSO VSX connector downloads.

The accepted bulk assets are the VSX object catalog, its bibliographic
reference table, and the small AAVSO photometric band codebook. The two large
tables come from the CDS VizieR TAP mirror; the codebook comes from the AAVSO
VSX JSON API because it is not exposed as a VizieR table.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, get, raw_parquet_writer, save_raw_parquet

_TAP_URL = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
_BANDS_URL = "https://vsx.aavso.org/index.php"
_USER_AGENT = "Mozilla/5.0 (compatible; subsets.io connector; +https://subsets.io)"

_VSX_SCHEMA = pa.schema(
    [
        ("recno", pa.int64()),
        ("OID", pa.int64()),
        ("Name", pa.string()),
        ("V", pa.int64()),
        ("RAJ2000", pa.float64()),
        ("DEJ2000", pa.float64()),
        ("Type", pa.string()),
        ("l_max", pa.string()),
        ("max", pa.float64()),
        ("u_max", pa.string()),
        ("n_max", pa.string()),
        ("f_min", pa.string()),
        ("l_min", pa.string()),
        ("min", pa.float64()),
        ("u_min", pa.string()),
        ("n_min", pa.string()),
        ("Epoch", pa.float64()),
        ("u_Epoch", pa.string()),
        ("l_Period", pa.string()),
        ("Period", pa.float64()),
        ("u_Period", pa.string()),
        ("Sp", pa.string()),
        ("n_OID", pa.string()),
    ]
)
_REFS_SCHEMA = pa.schema(
    [
        ("recno", pa.int64()),
        ("OID", pa.int64()),
        ("Bibcode", pa.string()),
    ]
)
_BANDS_SCHEMA = pa.schema(
    [
        ("Code", pa.int64()),
        ("Description", pa.string()),
        ("ShortName", pa.string()),
        ("RColor", pa.int64()),
        ("GColor", pa.int64()),
        ("BColor", pa.int64()),
        ("Picklist", pa.int64()),
        ("Weight", pa.int64()),
    ]
)

_PAGE_SIZE = 100_000
_TABLES = {
    "aavso-vsx-catalog": ("B/vsx/vsx", _VSX_SCHEMA, 400),
    "aavso-vsx-references": ("B/vsx/refs", _REFS_SCHEMA, 50),
}


def _schema_names(schema: pa.Schema) -> list[str]:
    return [field.name for field in schema]


def _csv_column_types(schema: pa.Schema) -> dict[str, pa.DataType]:
    return {field.name: field.type for field in schema}


def _fetch_tap_page(table_name: str, schema: pa.Schema, after_recno: int) -> pa.Table:
    cols = _schema_names(schema)
    query = (
        f'SELECT TOP {_PAGE_SIZE} {",".join(cols)} FROM "{table_name}" '
        f"WHERE recno > {after_recno} ORDER BY recno"
    )
    resp = get(
        _TAP_URL,
        params={"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "QUERY": query},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return pacsv.read_csv(
        io.BytesIO(resp.content),
        convert_options=pacsv.ConvertOptions(
            column_types=_csv_column_types(schema),
            strings_can_be_null=True,
        ),
    ).select(cols)


def fetch_tap_table(node_id: str) -> None:
    table_name, schema, max_pages = _TABLES[node_id]
    after_recno = 0
    pages = 0
    total = 0
    with raw_parquet_writer(node_id, schema) as writer:
        while True:
            if pages >= max_pages:
                raise RuntimeError(
                    f"{node_id}: hit safety cap of {max_pages} pages "
                    f"after recno={after_recno}; raise the cap if VSX grew"
                )
            table = _fetch_tap_page(table_name, schema, after_recno)
            pages += 1
            rows = table.num_rows
            if rows == 0:
                break
            writer.write_table(table)
            total += rows
            after_recno = table.column("recno")[rows - 1].as_py()
            if rows < _PAGE_SIZE:
                break
    print(f"{node_id}: wrote {total:,} rows over {pages} page(s)")


def _parse_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def fetch_photometric_bands(node_id: str) -> None:
    resp = get(
        _BANDS_URL,
        params={"view": "api.bands", "format": "json"},
        headers={"User-Agent": _USER_AGENT},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    records = resp.json().get("Bands", {}).get("Band", [])
    rows = [
        {
            "Code": _parse_int(row.get("Code")),
            "Description": row.get("Description"),
            "ShortName": row.get("ShortName"),
            "RColor": _parse_int(row.get("RColor")),
            "GColor": _parse_int(row.get("GColor")),
            "BColor": _parse_int(row.get("BColor")),
            "Picklist": _parse_int(row.get("Picklist")),
            "Weight": _parse_int(row.get("Weight")),
        }
        for row in records
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_BANDS_SCHEMA), node_id)
    print(f"{node_id}: wrote {len(rows):,} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="aavso-photometric-bands", fn=fetch_photometric_bands, kind="download"),
    NodeSpec(id="aavso-vsx-catalog", fn=fetch_tap_table, kind="download"),
    NodeSpec(id="aavso-vsx-references", fn=fetch_tap_table, kind="download"),
]
