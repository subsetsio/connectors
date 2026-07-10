"""FEC independent expenditures: plain header'd CSVs (one per cycle, not
zipped). Headers drift across cycles, so each cycle is aligned to the canonical
IE_COLS (missing columns backfilled null) before concat."""

from __future__ import annotations

import os

import duckdb
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BULK, _bytes_to_tempfile, _cycles, _ie_get

# Independent expenditures CSV carries its own (lowercase) header. Canonical
# column set from recent cycles; older cycles may omit trailing columns, which
# are backfilled as null during alignment.
IE_COLS = [
    "cand_id", "cand_name", "spe_id", "spe_nam", "ele_type",
    "can_office_state", "can_office_dis", "can_office", "cand_pty_aff",
    "exp_amo", "exp_date", "agg_amo", "sup_opp", "pur", "pay", "file_num",
    "amndt_ind", "tran_id", "image_num", "receipt_dat", "fec_election_yr",
    "prev_file_num", "dissem_dt",
]


def fetch_independent_expenditures(node_id: str) -> None:
    """Independent-expenditure files are plain header'd CSVs (one per cycle, not
    zipped). Headers drift across cycles, so each cycle is aligned to the
    canonical IE_COLS (missing columns backfilled null) before concat."""
    parts = []
    for cycle in _cycles():
        url = f"{BULK}/{cycle}/independent_expenditure_{cycle}.csv"
        resp = _ie_get(url)
        if resp is None:
            print(f"  {node_id}: IE {cycle} not published, skipping")
            continue
        path = _bytes_to_tempfile(resp)
        try:
            tbl = duckdb.sql(
                f"SELECT * FROM read_csv('{path}', header=true, "
                f"all_varchar=true, ignore_errors=true)"
            ).to_arrow_table()
        finally:
            os.unlink(path)
        present = set(tbl.column_names)
        arrays = [pa.array([cycle] * tbl.num_rows, pa.string())]
        for col in IE_COLS:
            if col in present:
                arrays.append(tbl.column(col).cast(pa.string()))
            else:
                arrays.append(pa.nulls(tbl.num_rows, pa.string()))
        parts.append(pa.table(arrays, names=["cycle"] + IE_COLS))
        print(f"  {node_id}: {cycle} -> {tbl.num_rows:,} rows")
    if not parts:
        raise RuntimeError(f"{node_id}: no cycles fetched")
    save_raw_parquet(pa.concat_tables(parts), node_id)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-independent-expenditures-transform",
        deps=["fec-independent-expenditures"],
        sql="""
            SELECT
                cycle,
                cand_id,
                cand_name,
                cand_pty_aff                              AS cand_party,
                can_office                                AS cand_office,
                can_office_state                          AS cand_office_state,
                can_office_dis                            AS cand_office_district,
                spe_id                                    AS spender_cmte_id,
                spe_nam                                   AS spender_name,
                sup_opp                                   AS support_oppose,
                ele_type                                  AS election_type,
                TRY_CAST(exp_amo AS DOUBLE)               AS amount,
                TRY_STRPTIME(exp_date, '%m/%d/%Y')::DATE  AS expenditure_date,
                TRY_CAST(agg_amo AS DOUBLE)               AS aggregate_amount,
                pur                                       AS purpose,
                pay                                       AS payee,
                TRY_CAST(file_num AS BIGINT)              AS file_num,
                tran_id,
                image_num,
                amndt_ind                                 AS amendment_ind,
                TRY_STRPTIME(receipt_dat, '%m/%d/%Y')::DATE AS receipt_date,
                TRY_CAST(fec_election_yr AS INTEGER)      AS fec_election_yr,
                TRY_STRPTIME(dissem_dt, '%m/%d/%Y')::DATE AS dissemination_date
            FROM "fec-independent-expenditures"
            WHERE spe_id IS NOT NULL AND spe_id <> ''
        """,
    ),
]
