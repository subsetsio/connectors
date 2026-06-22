"""CBS (Netherlands) — Statistics Netherlands open data (StatLine v4).

One published Delta table per CBS dataset. Each dataset is fetched as a single
ZIP from the v4 bulk-CSV distribution (https://datasets.cbs.nl/csv/CBS/nl/<id>),
which contains the full observation table plus every code/label table. We
unpack it in the fetch fn, resolve measure and dimension codes to their Dutch
labels, and write a uniform long-format ndjson raw asset so the SQL transform is
a thin, generic projection.

Fetch shape: stateless full re-pull (shape 1). Each dataset is one stable URL
returning the complete table in one request, so there is no watermark/cursor —
we re-download and overwrite every run, which picks up CBS revisions for free.
The largest datasets reach hundreds of millions of observations, so the ZIP is
streamed to a temp file and the Observations member is parsed row-by-row with
bounded memory (only the small code tables are held in RAM).
"""

import csv
import io
import json
import os
import tempfile
import zipfile

import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, get_client, transient_retry, raw_writer
from constants import ENTITY_IDS

# Map the (lossy) NodeSpec id back to the exact CBS Identifier. The spec id
# lowercases and dash-replaces (e.g. '70077NED' -> 'cbs-70077ned',
# '7052_95' -> 'cbs-7052-95'); the download URL needs the original casing.
_SPEC_TO_IDENT = {
    f"cbs-{e.lower().replace('_', '-')}": e for e in ENTITY_IDS
}

_BULK_URL = "https://datasets.cbs.nl/csv/CBS/nl/{ident}"

# Observations.csv fixed (non-dimension) columns.
_FIXED = {"Id", "Measure", "Value", "StringValue", "ValueAttribute"}
# CBS standard time dimension; promoted to the `period` columns.
_PERIOD_DIM = "Perioden"


@transient_retry()
def _download_zip(url: str, dest_path: str) -> None:
    """Stream the ZIP distribution to disk with bounded memory."""
    client = get_client()
    timeout = httpx.Timeout(connect=15.0, read=300.0, write=60.0, pool=60.0)
    with client.stream("GET", url, timeout=timeout) as resp:
        resp.raise_for_status()
        with open(dest_path, "wb") as fh:
            for chunk in resp.iter_bytes(1 << 20):
                fh.write(chunk)


def _read_csv(zf: zipfile.ZipFile, member: str):
    """Yield rows (dicts) from a semicolon-delimited CBS CSV member.

    Uses utf-8-sig to strip a leading BOM and the csv module to honour quoted
    multi-line fields (CBS Description columns contain embedded newlines).
    """
    with zf.open(member) as raw:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig"), delimiter=";")
        for row in reader:
            yield row


def _load_labels(zf: zipfile.ZipFile, members: set):
    """Build the measure and per-dimension code->label maps held in memory.

    Returns (measure_meta, dim_labels) where measure_meta maps a measure code to
    (title, unit) and dim_labels maps a dimension name to {code: title}.
    """
    measure_meta = {}
    if "MeasureCodes.csv" in members:
        for r in _read_csv(zf, "MeasureCodes.csv"):
            ident = r.get("Identifier")
            if ident is None:
                continue
            unit = (r.get("Unit") or "").strip() or None
            measure_meta[ident] = (r.get("Title"), unit)

    # Dimensions.csv tells us each dimension's CodesUrl; fall back to the
    # conventional "<Dim>Codes.csv" name when the column is absent.
    dim_codes_file = {}
    if "Dimensions.csv" in members:
        for r in _read_csv(zf, "Dimensions.csv"):
            dim = r.get("Identifier")
            if not dim:
                continue
            url = (r.get("CodesUrl") or "").strip()
            dim_codes_file[dim] = url or f"{dim}Codes.csv"

    dim_labels = {}
    for dim, fname in dim_codes_file.items():
        if fname not in members:
            continue
        labels = {}
        for r in _read_csv(zf, fname):
            code = r.get("Identifier")
            if code is not None:
                labels[code] = r.get("Title")
        dim_labels[dim] = labels
    return measure_meta, dim_labels


def _parse_value(raw):
    """CBS uses a decimal comma ('7888,2'). Return float or None."""
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the raw asset name
    ident = _SPEC_TO_IDENT[node_id]
    url = _BULK_URL.format(ident=ident)

    tmp = tempfile.NamedTemporaryFile(prefix="cbs_", suffix=".zip", delete=False)
    tmp.close()
    try:
        _download_zip(url, tmp.name)
        with zipfile.ZipFile(tmp.name) as zf:
            members = set(zf.namelist())
            measure_meta, dim_labels = _load_labels(zf, members)

            # Read the Observations header to learn the dimension columns and
            # their order, then stream the body row-by-row into ndjson.
            with zf.open("Observations.csv") as raw:
                text = io.TextIOWrapper(raw, encoding="utf-8-sig")
                reader = csv.reader(text, delimiter=";")
                header = next(reader)
                pos = {name: i for i, name in enumerate(header)}
                dim_cols = [h for h in header if h not in _FIXED]
                has_period = _PERIOD_DIM in dim_cols
                other_dims = [d for d in dim_cols if d != _PERIOD_DIM]

                i_measure = pos.get("Measure")
                i_value = pos.get("Value")
                i_string = pos.get("StringValue")
                i_period = pos.get(_PERIOD_DIM)

                with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
                    for row in reader:
                        if i_measure is None or i_measure >= len(row):
                            continue
                        mcode = row[i_measure]
                        mtitle, munit = measure_meta.get(mcode, (None, None))

                        rec = {
                            "measure": mcode,
                            "measure_label": mtitle,
                            "unit": munit,
                        }
                        if has_period and i_period is not None and i_period < len(row):
                            pcode = row[i_period]
                            rec["period"] = pcode or None
                            rec["period_label"] = dim_labels.get(_PERIOD_DIM, {}).get(pcode, pcode)
                        else:
                            rec["period"] = None
                            rec["period_label"] = None

                        for dim in other_dims:
                            di = pos[dim]
                            code = row[di] if di < len(row) else None
                            rec[dim] = dim_labels.get(dim, {}).get(code, code)

                        rec["value"] = _parse_value(row[i_value]) if i_value is not None and i_value < len(row) else None
                        sval = row[i_string] if i_string is not None and i_string < len(row) else None
                        rec["string_value"] = (sval or None) if sval is not None else None

                        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cbs-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Generic thin projection: the fetch fn already produced clean, typed,
# label-resolved long-format rows, so the transform just publishes the table
# (one Delta table per dataset) and drops rows with no observed value.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT *
            FROM "{s.id}"
            WHERE value IS NOT NULL OR string_value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
