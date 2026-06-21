"""npm-package-versions — per-(package, version) publish timeline.

No incremental query support on the packument endpoint, so the package head is
re-fetched in full every run.
"""
from urllib.parse import quote

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import REGISTRY_URL, _get_resp, _popular_names

_VERSIONS_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("version", pa.string()),
    ("published_at", pa.string()),
    ("deprecated", pa.bool_()),
    ("deprecation_message", pa.string()),
    ("dependencies_count", pa.int32()),
    ("dev_dependencies_count", pa.int32()),
    ("unpacked_size_bytes", pa.int64()),
])


def _rows_from_packument(doc: dict) -> list[dict]:
    name = doc.get("name")
    times = doc.get("time") or {}
    versions = doc.get("versions") or {}
    rows = []
    for version, vdoc in versions.items():
        dep_val = vdoc.get("deprecated")
        dist = vdoc.get("dist") or {}
        unpacked = dist.get("unpackedSize")
        rows.append({
            "package": name,
            "version": version,
            "published_at": times.get(version),
            "deprecated": bool(dep_val),
            "deprecation_message": dep_val if isinstance(dep_val, str) else None,
            "dependencies_count": len(vdoc.get("dependencies") or {}),
            "dev_dependencies_count": len(vdoc.get("devDependencies") or {}),
            "unpacked_size_bytes": int(unpacked) if unpacked is not None else None,
        })
    return rows


def fetch_package_versions(node_id: str) -> None:
    names = _popular_names()
    print(f"  {node_id}: {len(names):,} packuments to fetch")
    rows: list[dict] = []
    for i, name in enumerate(names):
        resp = _get_resp(f"{REGISTRY_URL}/{quote(name, safe='@/')}")
        if resp is not None:
            rows.extend(_rows_from_packument(resp.json()))
        if (i + 1) % 250 == 0:
            print(f"    {i + 1:,}/{len(names):,} ({len(rows):,} version rows)")
    table = pa.Table.from_pylist(rows, schema=_VERSIONS_SCHEMA)
    save_raw_parquet(table, node_id)
    print(f"  {node_id}: {table.num_rows:,} version rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="npm-package-versions", fn=fetch_package_versions, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="npm-package-versions-transform",
        deps=["npm-package-versions"],
        sql='''
            SELECT
                package,
                version,
                CAST(published_at AS TIMESTAMP)         AS published_at,
                deprecated,
                deprecation_message,
                CAST(dependencies_count AS INTEGER)     AS dependencies_count,
                CAST(dev_dependencies_count AS INTEGER) AS dev_dependencies_count,
                CAST(unpacked_size_bytes AS BIGINT)     AS unpacked_size_bytes
            FROM "npm-package-versions"
            WHERE package IS NOT NULL AND version IS NOT NULL
        ''',
    ),
]
