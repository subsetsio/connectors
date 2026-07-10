"""FEC candidate-committee linkages (ccl): headerless pipe file fetched across
all cycles via the shared simple loader."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import _save_simple

CCL_COLS = [
    "CAND_ID", "CAND_ELECTION_YR", "FEC_ELECTION_YR", "CMTE_ID", "CMTE_TP",
    "CMTE_DSGN", "LINKAGE_ID",
]


def fetch_linkages(node_id: str) -> None:
    _save_simple(node_id, "ccl", CCL_COLS)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fec-candidate-committee-linkages-transform",
        deps=["fec-candidate-committee-linkages"],
        sql="""
            SELECT
                cycle,
                LINKAGE_ID                                AS linkage_id,
                CAND_ID                                   AS cand_id,
                CMTE_ID                                   AS cmte_id,
                CMTE_TP                                   AS cmte_type,
                CMTE_DSGN                                 AS cmte_designation,
                TRY_CAST(CAND_ELECTION_YR AS INTEGER)     AS cand_election_yr,
                TRY_CAST(FEC_ELECTION_YR AS INTEGER)      AS fec_election_yr
            FROM "fec-candidate-committee-linkages"
            WHERE LINKAGE_ID IS NOT NULL AND LINKAGE_ID <> ''
            QUALIFY row_number() OVER (
                PARTITION BY cycle, LINKAGE_ID ORDER BY CMTE_ID
            ) = 1
        """,
    ),
]
