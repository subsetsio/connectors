"""Connector-local runtime hooks for OSV.

OSV's advisory table preserves several nested JSON fields as strings. The
complete export can exceed DuckDB's default Arrow string-buffer ceiling while
streaming the transform into Delta, so enable large Arrow buffers for this
connector's SQL transform subprocesses.
"""

import duckdb

from subsets_utils.sql_transform import run_sql_node as _run_sql_node


def run_sql_node(spec) -> None:
    duckdb.sql("SET arrow_large_buffer_size=true")
    _run_sql_node(spec)
