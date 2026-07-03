"""UCDP connector — Uppsala Conflict Data Program.

Mechanism: public bulk download (https://ucdp.uu.se/downloads/). One stable,
versioned, public URL per dataset returns the entire table in one request — no
auth, no pagination (the token-gated REST API is deliberately ignored per
research). This is a catalog connector: every accepted collect entity is fetched
the same way via `fetch_one`, which recovers the entity from its node id.

Three payload shapes are handled:
  - csv_zip : a .zip wrapping exactly one CSV  (GED, the yearly conflict files)
  - csv     : a bare CSV                       (onset, candidate GED, CACE, DECO...)
  - dta_zip : a .zip of Stata .dta files       (External Support Dataset, no CSV)

CSVs are parsed with pyarrow's CSV reader (auto type inference is sound here:
each asset is one single-shot write, not a batched/repeated write, so there is
no cross-batch drift to guard against) and the delimiter is sniffed from the
header (CACE uses ';', the rest ','). Stata files are read with pandas. Every
asset lands as a single zstd parquet via save_raw_parquet.
"""
import io
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet

# entity_id -> (url, kind[, dta_member])
#   kind: "csv_zip" | "csv" | "dta_zip"
#   dta_member (dta_zip only): basename of the .dta to extract — the esd-ty zip
#   is a bundle holding all three files, so we must select by name.
ENTITY_META = {
    "actor": ("https://ucdp.uu.se/downloads/actor/ucdp-actor-261-csv.zip", "csv_zip"),
    "brd-conf": ("https://ucdp.uu.se/downloads/brd/ucdp-brd-conf-261-csv.zip", "csv_zip"),
    "brd-dyadic": ("https://ucdp.uu.se/downloads/brd/ucdp-brd-dyadic-261-csv.zip", "csv_zip"),
    "cace": ("https://ucdp.uu.se/downloads/cace/CACE_1989-2017.csv", "csv"),
    "candidate-ged": ("https://ucdp.uu.se/downloads/candidateged/GEDEvent_v26_0_4.csv", "csv"),
    "cid-dyadissueyear": ("https://ucdp.uu.se/downloads/cid/ucdp_issues_dataset_dyadissueyear_232.csv", "csv"),
    "cid-dyadyear": ("https://ucdp.uu.se/downloads/cid/ucdp_issues_dataset_dyadyear_232.csv", "csv"),
    "deco": ("https://ucdp.uu.se/downloads/deco/DECO_v.1.0.csv", "csv"),
    "dyadic": ("https://ucdp.uu.se/downloads/dyadic/ucdp-dyadic-261-csv.zip", "csv_zip"),
    "esd-ay": ("https://ucdp.uu.se/downloads/extsup/ESD/ucdp-esd-ay-181.zip", "dta_zip", "ucdp-esd-ay-181.dta"),
    "esd-dy": ("https://ucdp.uu.se/downloads/extsup/ESD/ucdp-esd-dy-181.zip", "dta_zip", "ucdp-esd-dy-181.dta"),
    "esd-ty": ("https://ucdp.uu.se/downloads/extsup/ESD/ucdp-esd-ty-181.zip", "dta_zip", "ucdp-esd-ty-181.dta"),
    "ged": ("https://ucdp.uu.se/downloads/ged/ged261-csv.zip", "csv_zip"),
    "nonstate": ("https://ucdp.uu.se/downloads/nsos/ucdp-nonstate-261-csv.zip", "csv_zip"),
    "onesided": ("https://ucdp.uu.se/downloads/nsos/ucdp-onesided-261-csv.zip", "csv_zip"),
    "onset-interstate-conflict": ("https://ucdp.uu.se/downloads/onset/ucdp-interstate-conflict-onset-251.csv", "csv"),
    "onset-intrastate-conflict": ("https://ucdp.uu.se/downloads/onset/ucdp-intrastate-conflict-onset-251.csv", "csv"),
    "onset-intrastate-country": ("https://ucdp.uu.se/downloads/onset/ucdp-intrastate-country-onset-251.csv", "csv"),
    "organizedviolencecy": ("https://ucdp.uu.se/downloads/organizedviolencecy/organizedviolencecy-261-csv.zip", "csv_zip"),
    "term-conflict": ("https://ucdp.uu.se/downloads/monadterm/UCDPConflictTerminationDataset_v4_2024_Conflict.csv", "csv"),
    "term-dyad": ("https://ucdp.uu.se/downloads/monadterm/UCDPConflictTerminationDataset_v4_2024_Dyad.csv", "csv"),
    "ucdp-prio-acd": ("https://ucdp.uu.se/downloads/ucdpprio/ucdp-prio-acd-261-csv.zip", "csv_zip"),
    "vpp-ged": ("https://ucdp.uu.se/downloads/vpp/GEDEvent_v26_1_4_1101_2512.csv", "csv"),
}

# Entity union (rank-accepted) — copied from work/entity_union.json.
ENTITY_IDS = sorted(ENTITY_META)

_PREFIX = "ucdp-"


def _entity_from_node(node_id: str) -> str:
    """Recover the collect entity id from the node/spec id."""
    assert node_id.startswith(_PREFIX), f"unexpected node id {node_id!r}"
    return node_id[len(_PREFIX):]


def _sniff_delimiter(data: bytes) -> str:
    """UCDP CSVs are comma-separated except CACE, which is semicolon. Decide
    from the header line by counting candidate delimiters outside the obvious."""
    first = data.split(b"\n", 1)[0]
    return ";" if first.count(b";") > first.count(b",") else ","


def _csv_bytes_to_table(data: bytes) -> pa.Table:
    delimiter = _sniff_delimiter(data)
    return pacsv.read_csv(
        io.BytesIO(data),
        # newlines_in_values: GED free-text fields (source_article, location
        # names) contain embedded newlines inside quoted values; without this
        # pyarrow splits a row early and the column count breaks.
        parse_options=pacsv.ParseOptions(delimiter=delimiter, newlines_in_values=True),
        # Treat empty strings and common UCDP sentinels as null during inference.
        convert_options=pacsv.ConvertOptions(strings_can_be_null=True),
    )


def _dta_bytes_to_table(data: bytes) -> pa.Table:
    import pandas as pd

    df = pd.read_stata(io.BytesIO(data), convert_categoricals=False)
    return pa.Table.from_pandas(df, preserve_index=False)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it is the asset name
    entity = _entity_from_node(node_id)
    meta = ENTITY_META[entity]
    url, kind = meta[0], meta[1]

    resp = get(url, timeout=600)
    resp.raise_for_status()
    content = resp.content

    if kind == "csv":
        table = _csv_bytes_to_table(content)

    elif kind == "csv_zip":
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            assert len(members) == 1, f"{asset}: expected 1 CSV in zip, got {members}"
            table = _csv_bytes_to_table(zf.read(members[0]))

    elif kind == "dta_zip":
        target = meta[2]
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            matches = [n for n in zf.namelist() if n.rsplit("/", 1)[-1] == target]
            assert matches, f"{asset}: {target} not found in zip ({zf.namelist()})"
            table = _dta_bytes_to_table(zf.read(matches[0]))

    else:  # pragma: no cover - guarded by ENTITY_META authoring
        raise ValueError(f"{asset}: unknown kind {kind!r}")

    assert table.num_rows > 0, f"{asset}: parsed 0 rows from {url}"
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{_PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# Per-dataset grain declarations (entity id -> optional key/temporal kwargs).
# Event-level datasets (the GED family, CACE, DECO, the External Support
# Datasets) carry a genuine unique event/row id, verified unique in the profile.
# The yearly conflict/dyad/country panels get their observation period (year)
# but no key — their composite grain is not verified unique here, so declaring
# one is unsafe. Entities absent from this map (e.g. actor) stay undeclared.
GRAINS = {
    "cace": {"key": ("id",), "temporal": "year"},
    "candidate-ged": {"key": ("id",), "temporal": "date_start"},
    "deco": {"key": ("id",), "temporal": "year"},
    "esd-ay": {"key": ("id",), "temporal": "year"},
    "esd-dy": {"key": ("id",), "temporal": "year"},
    "esd-ty": {"key": ("id",), "temporal": "year"},
    "ged": {"key": ("id",), "temporal": "date_start"},
    "vpp-ged": {"key": ("id",), "temporal": "date_start"},
    "brd-conf": {"temporal": "year"},
    "brd-dyadic": {"temporal": "year"},
    "dyadic": {"temporal": "year"},
    "nonstate": {"temporal": "year"},
    "onesided": {"temporal": "year"},
    "term-conflict": {"temporal": "year"},
    "term-dyad": {"temporal": "year"},
    "ucdp-prio-acd": {"temporal": "year"},
    "organizedviolencecy": {"temporal": "year"},
    "onset-interstate-conflict": {"temporal": "year"},
    "onset-intrastate-conflict": {"temporal": "year"},
    "onset-intrastate-country": {"temporal": "year"},
    "cid-dyadyear": {"temporal": "year"},
    "cid-dyadissueyear": {"temporal": "year"},
}

# One published Delta table per dataset. The raw parquet is already clean,
# typed, full-snapshot tabular, so the transform is a straight pass-through; the
# runtime overwrites the table named (transform id minus "-transform").
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_PREFIX}{eid}-transform",
        deps=(f"{_PREFIX}{eid}",),
        sql=f'SELECT * FROM "{_PREFIX}{eid}"',
        **GRAINS.get(eid, {}),
    )
    for eid in ENTITY_IDS
]
