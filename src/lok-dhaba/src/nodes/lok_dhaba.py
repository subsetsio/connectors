"""Download nodes for Lok Dhaba election results."""

import csv
import gzip
import io

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

SLUG = "lok-dhaba"
BASE_URL = "https://lokdhaba.ashoka.edu.in/downloads/All_States"

GE_COLUMNS = [
    "State_Name", "Assembly_No", "Constituency_No", "Year", "month", "Poll_No",
    "DelimID", "Position", "Candidate", "Sex", "Party", "Votes",
    "Candidate_Type", "Valid_Votes", "Electors", "Constituency_Name",
    "Constituency_Type", "Sub_Region", "N_Cand", "Turnout_Percentage",
    "Vote_Share_Percentage", "Deposit_Lost", "Margin", "Margin_Percentage",
    "ENOP", "pid", "Party_Type_TCPD", "Party_ID", "last_poll", "Contested",
    "Last_Party", "Last_Party_ID", "Last_Constituency_Name",
    "Same_Constituency", "Same_Party", "No_Terms", "Turncoat", "Incumbent",
    "Recontest", "MyNeta_education", "TCPD_Prof_Main", "TCPD_Prof_Main_Desc",
    "TCPD_Prof_Second", "TCPD_Prof_Second_Desc", "Election_Type",
]

AE_COLUMNS = [
    "State_Name", "Assembly_No", "Constituency_No", "Year", "month", "DelimID",
    "Poll_No", "Position", "Candidate", "Sex", "Party", "Votes", "Age",
    "Candidate_Type", "Valid_Votes", "Electors", "Constituency_Name",
    "Constituency_Type", "District_Name", "Sub_Region", "N_Cand",
    "Turnout_Percentage", "Vote_Share_Percentage", "Deposit_Lost", "Margin",
    "Margin_Percentage", "ENOP", "pid", "Party_Type_TCPD", "Party_ID",
    "last_poll", "Contested", "Last_Party", "Last_Party_ID",
    "Last_Constituency_Name", "Same_Constituency", "Same_Party", "No_Terms",
    "Turncoat", "Incumbent", "Recontest", "MyNeta_education",
    "TCPD_Prof_Main", "TCPD_Prof_Main_Desc", "TCPD_Prof_Second",
    "TCPD_Prof_Second_Desc", "Election_Type",
]

GA_COLUMNS = [
    "Assembly_No", "State_Name", "Constituency_No", "Poll_No", "Year",
    "PC_Name", "PC_No", "Constituency_Name", "Constituency_Type", "CandID",
    "Candidate", "Party", "Votes", "Position", "N_Cand", "Valid_Votes",
    "Vote_Share_Percentage", "Deposit_Lost", "Margin", "Margin_Percentage",
    "ENOP", "Sex", "pid", "Candidate_Type", "DelimID", "Party_ID",
    "Party_Type_TCPD", "Contested", "Last_Party", "Last_Party_ID",
    "Last_Constituency_Name", "Same_Constituency", "Same_Party", "No_Terms",
    "Turncoat", "Incumbent", "Recontest", "MyNeta_education",
    "TCPD_Prof_Main", "TCPD_Prof_Main_Desc", "TCPD_Prof_Second",
    "TCPD_Prof_Second_Desc", "Election_Type",
]

CONFIG = {
    "general-election-results": ("All_States_GE.csv.gz", GE_COLUMNS),
    "assembly-election-results": ("All_States_AE.csv.gz", AE_COLUMNS),
    "general-election-segment-results": ("All_States_GA.csv.gz", GA_COLUMNS),
}


def _entity_id(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id[len(prefix):]


def _url_for_entity(entity_id: str) -> str:
    filename, _columns = CONFIG[entity_id]
    return f"{BASE_URL}/{filename}"


def _table_from_csv_gz(content: bytes, columns: list[str]) -> pa.Table:
    text = gzip.decompress(content).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != columns:
        raise ValueError(
            f"unexpected CSV header: got {reader.fieldnames!r}, expected {columns!r}"
        )

    rows = list(reader)
    schema = pa.schema([(name, pa.string()) for name in columns])
    arrays = [
        pa.array([(row.get(name) or None) for row in rows], type=pa.string())
        for name in columns
    ]
    return pa.Table.from_arrays(arrays, schema=schema)


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    _filename, columns = CONFIG[entity_id]
    url = _url_for_entity(entity_id)

    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    table = _table_from_csv_gz(resp.content, columns)
    if table.num_rows == 0:
        raise ValueError(f"{node_id}: downloaded CSV has no rows")

    save_raw_parquet(table, node_id)
    record_source_signature(node_id, url, response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(id="lok-dhaba-assembly-election-results", fn=fetch_one, kind="download"),
    NodeSpec(id="lok-dhaba-general-election-results", fn=fetch_one, kind="download"),
    NodeSpec(id="lok-dhaba-general-election-segment-results", fn=fetch_one, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Refresh monthly; no published release cadence found. Static bulk "
            "CSV endpoints expose ETag/Last-Modified validators."
        ),
        check=lambda aid: source_unchanged(aid, _url_for_entity(_entity_id(aid)))
        and raw_asset_exists(aid, "parquet", max_age_days=45),
    )
    for spec in DOWNLOAD_SPECS
]
