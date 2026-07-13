"""UK Pollinator Monitoring Scheme raw downloads.

The current EIDC releases are versioned ZIP packages containing one CSV per
publishable table. We fetch the package, extract the selected CSV member, and
save it as parquet with source columns preserved as strings. Transforms own the
semantic typing once the raw shape has been profiled.
"""

from __future__ import annotations

import csv
import io
import zipfile

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet


_FIT_UUID = "699f2172-88c1-44b7-a8f5-a22296a9e2cb"
_PAN_UUID = "4a565007-d3a1-468d-9f84-70ec7594fafe"

_ENTITIES = {
    "uk-poms-ukpoms-1kmfitcountdata-2017-2022": {
        "uuid": _FIT_UUID,
        "member": "data/ukpoms_1kmfitcountdata_2017-2022.csv",
    },
    "uk-poms-ukpoms-publicfitcountdata-2017-2022": {
        "uuid": _FIT_UUID,
        "member": "data/ukpoms_publicfitcountdata_2017-2022.csv",
    },
    "uk-poms-ukpoms-1kmpantrapdata-2017-2022-flowers": {
        "uuid": _PAN_UUID,
        "member": "data/ukpoms_1kmpantrapdata_2017-2022_flowers.csv",
    },
    "uk-poms-ukpoms-1kmpantrapdata-2017-2022-insects": {
        "uuid": _PAN_UUID,
        "member": "data/ukpoms_1kmpantrapdata_2017-2022_insects.csv",
    },
    "uk-poms-ukpoms-1kmpantrapdata-2017-2022-samples": {
        "uuid": _PAN_UUID,
        "member": "data/ukpoms_1kmpantrapdata_2017-2022_samples.csv",
    },
}


def _package_url(uuid: str) -> str:
    return f"https://data-package.ceh.ac.uk/data/{uuid}.zip"


def _csv_member(uuid: str, member: str) -> bytes:
    response = get(_package_url(uuid), timeout=(10.0, 120.0))
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        return archive.read(member)


def _csv_to_string_table(content: bytes) -> pa.Table:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("cp1252")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("CSV has no header")

    fieldnames = list(reader.fieldnames)
    columns = {name: [] for name in fieldnames}
    for row in reader:
        for name in fieldnames:
            columns[name].append(row.get(name))

    arrays = [pa.array(columns[name], type=pa.string()) for name in fieldnames]
    schema = pa.schema([(name, pa.string()) for name in fieldnames])
    return pa.Table.from_arrays(arrays, schema=schema)


def fetch_one(node_id: str) -> None:
    cfg = _ENTITIES[node_id]
    content = _csv_member(cfg["uuid"], cfg["member"])
    save_raw_parquet(_csv_to_string_table(content), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="uk-poms-ukpoms-1kmfitcountdata-2017-2022", fn=fetch_one, kind="download"),
    NodeSpec(id="uk-poms-ukpoms-publicfitcountdata-2017-2022", fn=fetch_one, kind="download"),
    NodeSpec(id="uk-poms-ukpoms-1kmpantrapdata-2017-2022-flowers", fn=fetch_one, kind="download"),
    NodeSpec(id="uk-poms-ukpoms-1kmpantrapdata-2017-2022-insects", fn=fetch_one, kind="download"),
    NodeSpec(id="uk-poms-ukpoms-1kmpantrapdata-2017-2022-samples", fn=fetch_one, kind="download"),
]
