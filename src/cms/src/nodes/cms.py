"""CMS connector — data.cms.gov open-data catalog + Provider Data Catalog (DKAN).

361 datasets across two sub-catalogs, each pulled as a single streamed bulk CSV
(the `bulk_csv_main` mechanism) rather than row-paginated — one request per
dataset keeps the run fast and gentle on the source (paginating the largest
datasets, ~28M rows, melted the server with 503s and could not finish in the
CI budget):

  * Main catalog (UUID ids) -> the data-api emits the full combined dataset as
    CSV in one shot:   GET /data-api/v1/dataset/{uuid}/data.csv
  * Provider Data Catalog (short/named ids) -> the DKAN datastore dumps the whole
    distribution as CSV: GET /provider-data/api/1/datastore/query/{id}/0/download?format=csv

Catalog scope is the queryable subset: collect drops the ~28 main datasets that
ship ONLY as ZIP bundles of yearly XLSX statistical reports ("CMS Program
Statistics", "MCBS COVID-19 Supplement", …) — they have no data-api/CSV
distribution (the data.csv endpoint hard-503s for them) and a multi-period
multi-sheet Excel bundle does not fit the one-clean-table-per-dataset model —
plus one verified-empty provider dataset (header-only CSV).

Stateless full re-pull each run (revisions picked up for free; no watermark
exists on the row data — catalogs expose only a dataset-level `modified` stamp a
later MaintainSpec can use to skip unchanged datasets).

Raw is written as all-string NDJSON, parsed with Python's lenient csv.reader.
CMS CSVs contain ragged rows and columns whose values drift type partway through
the file, so DuckDB's strict read_csv_auto (which the SQL transform would use on
a raw .csv) errors out on the large datasets; parsing to string NDJSON here and
letting the transform read_json_auto it back is robust. The transform is a thin
pass-through publishing one Delta table per dataset.
"""
import csv
import io
import json

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

MAIN_BASE = "https://data.cms.gov/data-api/v1/dataset"
PROV_BASE = "https://data.cms.gov/provider-data/api/1/datastore/query"
# Connect timeout, then a generous inter-chunk read timeout for multi-GB streams.
_TIMEOUT = httpx.Timeout(15.0, read=600.0)
_CHUNK = 1 << 20


class _ByteStream(io.RawIOBase):
    """Adapt an httpx byte-chunk iterator into a readable binary file object so
    csv.reader (via TextIOWrapper) can parse it streaming, bounded-memory, with
    correct handling of quoted fields that embed commas and newlines."""

    def __init__(self, chunks):
        self._it = iter(chunks)
        self._buf = b""

    def readable(self) -> bool:
        return True

    def readinto(self, b) -> int:
        while not self._buf:
            try:
                self._buf = next(self._it)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[:n], self._buf = self._buf[:n], self._buf[n:]
        return n


@transient_retry(attempts=8, min_wait=5, max_wait=240)
def _download_to_ndjson(url: str, asset: str) -> int:
    """Stream one dataset's CSV, parse to all-string row dicts, write NDJSON.

    Retried as a whole: a mid-stream transient error re-downloads from scratch
    and overwrites (raw_writer truncates on open), so partial files never leak.
    """
    client = get_client()
    n = 0
    with client.stream("GET", url, timeout=_TIMEOUT) as resp:
        resp.raise_for_status()
        binary = io.BufferedReader(_ByteStream(resp.iter_bytes(_CHUNK)))
        text = io.TextIOWrapper(binary, encoding="utf-8", errors="replace", newline="")
        reader = csv.reader(text)
        header = next(reader, None)
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
            if header is not None:
                width = len(header)
                for row in reader:
                    obj = {
                        header[i]: (row[i] if i < len(row) else None)
                        for i in range(width)
                    }
                    out.write(json.dumps(obj, separators=(",", ":")))
                    out.write("\n")
                    n += 1
    return n


def fetch_one(node_id: str) -> None:
    """Fetch one dataset (main or provider) as bulk CSV and stream it to NDJSON."""
    entity = _SPEC_TO_ENTITY[node_id]
    if entity in _MAIN_SET:
        url = f"{MAIN_BASE}/{entity}/data.csv"
    else:
        url = f"{PROV_BASE}/{entity}/0/download?format=csv"
    n = _download_to_ndjson(url, node_id)
    print(f"{node_id}: wrote {n:,} rows")


from constants import MAIN_IDS

from constants import PROVIDER_IDS

ENTITY_IDS = MAIN_IDS + PROVIDER_IDS
_MAIN_SET = set(MAIN_IDS)
# spec id -> original catalog entity id (lossless reverse of the id transform)
_SPEC_TO_ENTITY = {
    f"cms-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cms-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset. Each dataset has its own column set, so
# the transform is an honest pass-through over the NDJSON view (read_json_auto
# yields VARCHAR columns straight from the published CSV values).
#
# `SET arrow_large_buffer_size=true` makes DuckDB export string columns as Arrow
# large_string (64-bit offsets). The largest CMS datasets carry a text column
# whose concatenated bytes exceed the 2 GiB regular-string-buffer limit, which
# otherwise fails the Arrow record-batch export ("maximum total string size for
# regular string buffers is 2147483647"). large_string stores identically in
# parquet/Delta, so this is harmless for the small datasets and required for the
# few huge ones.
# Per-dataset grain / observation-period declarations. These 361 datasets are
# heterogeneous CSV pass-throughs (no QUALIFY / GROUP BY to read a grain from),
# so the declarations below are derived from the published profile: a KEY is
# declared only where a single column was observed unique across ALL rows AND is
# an unambiguous identifier (CCN, NPI, Facility ID, zip_code, enrollment id, …) —
# coincidentally-unique value/amount/name columns are deliberately excluded. A
# TEMPORAL is declared only where the profile's freshness column is a genuine
# reporting period (year / processing date / work date), never a registry event
# date (incorporation, revalidation-due, effective, termination, …). Datasets
# without a confident signal are left undeclared (safe). The dicts are a purely
# declarative lookup keyed by download-spec id.
_KEY = {
    "cms-0127-af37": ("zip_code",),
    "cms-029b-dd7e": ("zip_code",),
    "cms-0330-b6e0": ("zip_code",),
    "cms-057a-5bcf": ("zip_code",),
    "cms-069d-826b": ("zip_code",),
    "cms-075a-d487": ("zip_code",),
    "cms-086e48c4-87a6-4be1-8823-29e8da8f225b": ("prvdr_num",),
    "cms-0938-3dfa": ("zip_code",),
    "cms-0b1a-da3f": ("zip_code",),
    "cms-0d7d-e988": ("zip_code",),
    "cms-0ddf-4325": ("zip_code",),
    "cms-0f37-cab0": ("zip_code",),
    "cms-0f6a-98c3": ("zip_code",),
    "cms-129a6503-c0f1-4132-b186-4c0232c2d894": ("Provider Number",),
    "cms-14d8e8a9-7e9b-4370-a044-bf97c46b4b44": ("PRSCRBR_NPI",),
    "cms-23ew-n7w9": ("CMS Certification Number (CCN)",),
    "cms-2457ea29-fc82-48b0-86ec-3b0755de7515": ("ENRLMT_ID",),
    "cms-2483-f62b": ("zip_code",),
    "cms-254e-694c": ("zip_code",),
    "cms-261b83b6-b89f-43ad-ae7b-0d419a3bc24b": ("NPI",),
    "cms-284v-j9fz": ("CMS Certification Number (CCN)",),
    "cms-288b-4bed": ("zip_code",),
    "cms-2ca5-1007": ("zip_code",),
    "cms-2e55-8767": ("zip_code",),
    "cms-2fbd-6172": ("zip_code",),
    "cms-2fpu-cgbb": ("State",),
    "cms-32b2-9f88": ("zip_code",),
    "cms-32d8-3235": ("zip_code",),
    "cms-3614-1eef": ("zip_code",),
    "cms-385c-8c97": ("zip_code",),
    "cms-39da-b8ab": ("zip_code",),
    "cms-3a83-ee2d": ("zip_code",),
    "cms-3f64-129e": ("zip_code",),
    "cms-4269-8a74": ("zip_code",),
    "cms-44060663-47d8-4ced-a115-b53b4c270acb": ("rpt_rec_num",),
    "cms-44e93e18-b9b3-4650-9471-2b1b31dc588b": ("Unique ID",),
    "cms-4533-9861": ("zip_code",),
    "cms-48nr-hqxx": ("Facility ID",),
    "cms-4a4e-e0da": ("zip_code",),
    "cms-4bae4223-a1dc-4b9c-bd7e-d9622461be35": ("AGG_ID",),
    "cms-4j6d-yzce": ("Measure ID",),
    "cms-4pq5-n9py": ("CMS Certification Number (CCN)",),
    "cms-501b-ecd4": ("zip_code",),
    "cms-57e0-2991": ("zip_code",),
    "cms-59mq-zhts": ("CMS Certification Number (CCN)",),
    "cms-5d65-6dcf": ("zip_code",),
    "cms-5d9c-1e86": ("zip_code",),
    "cms-5e3a-bee4": ("zip_code",),
    "cms-5f44-cb84": ("zip_code",),
    "cms-5hk7-b79m": ("Facility ID",),
    "cms-6787-a1bf": ("zip_code",),
    "cms-69ec2609-5ce5-4ce1-b14c-1f8809fda2c2": ("aco_id",),
    "cms-6a0dbf98-e4b0-4037-ac63-1439b08f4a71": ("AGG_ID",),
    "cms-6b8f-5372": ("zip_code",),
    "cms-6bd6b1dd-208c-4f9c-88b8-b15fec6db548": ("NPI",),
    "cms-6jpm-sxkc": ("CMS Certification Number (CCN)",),
    "cms-730a-fcd0": ("zip_code",),
    "cms-7cf9662e-7c5c-4fe0-a8c6-828edf81a23c": ("HOSP_ID",),
    "cms-7t8x-u3ir": ("CMS Certification Number (CCN)",),
    "cms-8283-8a65": ("zip_code",),
    "cms-8634-f6a7": ("zip_code",),
    "cms-86e1-d1d1": ("zip_code",),
    "cms-8753-38d1": ("zip_code",),
    "cms-8889d81e-2ee7-448f-8713-f071038289b5": ("Rndrng_NPI",),
    "cms-8c6b-fe40": ("zip_code",),
    "cms-8c8a-b911": ("zip_code",),
    "cms-914a-7700": ("zip_code",),
    "cms-92bb-de79": ("zip_code",),
    "cms-94f7-ab53": ("zip_code",),
    "cms-9735-7176": ("zip_code",),
    "cms-9873-722a": ("zip_code",),
    "cms-98d4-0871": ("zip_code",),
    "cms-993f-4504": ("zip_code",),
    "cms-9b4a-75d5": ("zip_code",),
    "cms-a0cb-cdab": ("zip_code",),
    "cms-a15c198e-4cf3-46ab-a30e-15c69bd13edd": ("Unique ID",),
    "cms-a2d56d3f-3531-4315-9d87-e29986516b41": ("Suplr_NPI",),
    "cms-a6496a7d-4e19-479a-a9ad-d4c0a49e07c3": ("ENRLMT_ID",),
    "cms-a69d3df7-3f66-4a0d-b5b8-0d66049bd565": ("rpt_rec_num",),
    "cms-adba-1d45": ("zip_code",),
    "cms-afcb-07d8": ("zip_code",),
    "cms-avtz-f2ge": ("Facility ID",),
    "cms-axe7-s95e": ("State",),
    "cms-b06f-0828": ("zip_code",),
    "cms-b554-ef7e": ("zip_code",),
    "cms-b599-54c1": ("zip_code",),
    "cms-b9bf-6883": ("zip_code",),
    "cms-bb4c-dcdf": ("zip_code",),
    "cms-bce0-b5db": ("zip_code",),
    "cms-bd7d-078a": ("zip_code",),
    "cms-bdd5-4a04": ("zip_code",),
    "cms-c14e-6492": ("zip_code",),
    "cms-c382-eab7": ("zip_code",),
    "cms-c3e8e9c3-5193-47fb-a5bb-d3ddb00e7197": ("practice_id",),
    "cms-c44d-bde6": ("zip_code",),
    "cms-c713-00e8": ("zip_code",),
    "cms-c8a8-342e": ("zip_code",),
    "cms-ccbb-cbfa": ("zip_code",),
    "cms-ccn4-8vby": ("CMS Certification Number (CCN)",),
    "cms-cd1d-5f84": ("zip_code",),
    "cms-cfa7-e909": ("zip_code",),
    "cms-clinical-depression": ("CMS Certification Number (CCN)",),
    "cms-complete-qip-data": ("CMS Certification Number (CCN)",),
    "cms-covid-19-hcp": ("CMS Certification Number (CCN)",),
    "cms-ct36-nrcq": ("provider_id",),
    "cms-d0ce-5cad": ("zip_code",),
    "cms-d150-d141": ("zip_code",),
    "cms-d1c9-d5b4": ("zip_code",),
    "cms-d226-80a4": ("zip_code",),
    "cms-d3eb38ac-d8e9-40d3-b7b7-6205d3d1dc16": ("PRVDR_NUM",),
    "cms-d640-e528": ("zip_code",),
    "cms-d796-7f06": ("zip_code",),
    "cms-dgmq-aat3": ("Facility ID",),
    "cms-e1a1-c9b4": ("zip_code",),
    "cms-e2bb-d371": ("zip_code",),
    "cms-e491-a466": ("zip_code",),
    "cms-e84d-d357": ("zip_code",),
    "cms-ea2d-9467": ("zip_code",),
    "cms-ecb7-cb46": ("zip_code",),
    "cms-f226-42b7": ("zip_code",),
    "cms-f4ga-b9gx": ("Facility ID",),
    "cms-f557a6ed-95b3-4a22-8433-4175db2dec1c": ("ENROLLMENT ID - SELLER",),
    "cms-f8603e5b-9c47-4c52-9b47-a4ef92dfada4": ("Rfrg_NPI",),
    "cms-f90c-2246": ("zip_code",),
    "cms-fbfb-4b94": ("zip_code",),
    "cms-fche": ("CMS Certification Number (CCN)",),
    "cms-hanv-ru8h": ("STATE",),
    "cms-hypercalcemia": ("CMS Certification Number (CCN)",),
    "cms-ktv-comprehensive": ("CMS Certification Number (CCN)",),
    "cms-medrec": ("CMS Certification Number (CCN)",),
    "cms-mxtu-43qs": ("Facility ID",),
    "cms-nasn-k89k": ("Measure Code",),
    "cms-nhsn-bsi": ("CMS Certification Number (CCN)",),
    "cms-nhsn-de": ("CMS Certification Number (CCN)",),
    "cms-pppw": ("CMS Certification Number (CCN)",),
    "cms-pudb-wetr": ("Facility ID",),
    "cms-qip-ich-cahps": ("CMS Certification Number (CCN)",),
    "cms-rrqw-56er": ("Facility ID",),
    "cms-rs6n-9qwg": ("State",),
    "cms-shr": ("CMS Certification Number (CCN)",),
    "cms-srr": ("CMS Certification Number (CCN)",),
    "cms-strr": ("CMS Certification Number (CCN)",),
    "cms-su9h-3pvj": ("Facility ID",),
    "cms-tagd-9999": ("Deficiency Prefix and Number",),
    "cms-tee5-ixt5": ("State",),
    "cms-tps": ("CMS Certification Number (CCN)",),
    "cms-tqkv-mgxq": ("Facility ID",),
    "cms-vat-topic": ("CMS Certification Number (CCN)",),
    "cms-x663-bwbj": ("State",),
    "cms-xubh-q36u": ("Facility ID",),
    "cms-yc9t-dgbk": ("CMS Certification Number (CCN)",),
    "cms-ypbt-wvdk": ("Facility ID",),
    "cms-yq43-i98g": ("Facility ID",),
}

_TEMPORAL = {
    "cms-041d68a9-3212-42f3-89d5-b23e82103576": "PERF_YR",
    "cms-0764d86c-d19c-4b73-9e57-eba3cc1f7849": "Year",
    "cms-086e48c4-87a6-4be1-8823-29e8da8f225b": "processing_date",
    "cms-0d9eebff-7e23-4b1e-8e29-362eea132df5": "YEAR",
    "cms-1cd9eded-d2c9-4215-a064-aac6dae3b714": "year",
    "cms-2684c3e2-3598-4997-a598-0991bad6fbf2": "Year",
    "cms-2935c3fe-b18a-4e39-a0c5-e70573664f19": "YEAR",
    "cms-43ef03ce-2b60-40a8-958e-146195b5fec7": "YEAR",
    "cms-4c2a8bf6-8560-4b00-bc56-1a0322677b7f": "YEAR",
    "cms-4c74-462e": "Model Baseline Year",
    "cms-4ce4157f-4e02-4188-b43a-2b21b7769b4e": "Date",
    "cms-4e73f1b5-82cb-4682-8ad2-28493f0b6840": "YEAR",
    "cms-4jcv-atw7": "Year",
    "cms-4pq5-n9py": "Processing Date",
    "cms-54551982-39a8-4744-90f6-c38bb4dd5108": "perf_year",
    "cms-5f9f1216-6fd9-455d-bfbc-0efade687a4e": "YEAR",
    "cms-62e62d07-1837-4dbf-bb4f-a4820e0c7b16": "YEAR",
    "cms-6c3532b3-8325-48fd-a939-12b41d2b126a": "FIRST_PART_YEAR",
    "cms-6c63099b-0794-40a0-925c-51a66b9b9901": "YEAR",
    "cms-7e0d53ba-8f02-4c66-98a5-14a1c997c50d": "WorkDate",
    "cms-8e989bc0-2260-49a7-9c6d-8e9e10af7cea": "YEAR",
    "cms-939226be-b107-476e-8777-f199a840138a": "Year",
    "cms-94d00f36-73ce-4520-9b3f-83cd3cded25c": "Year",
    "cms-a93f5362-2fe6-4b4d-8260-118be0d618e0": "Calendar Year",
    "cms-ae8c9418-acc9-4442-b217-33291448f6b8": "Year",
    "cms-avtz-f2ge": "Fiscal Year",
    "cms-axe7-s95e": "Year",
    "cms-b497431a-5b57-42c0-9016-90105b51841e": "WorkDate",
    "cms-bb2a336c-0710-4de9-80ad-6a2a5cbdbdeb": "PERF_YR",
    "cms-c0451a3a-a86c-4bd4-a0b7-c93e6b1f1257": "Year of publication",
    "cms-c37ebe6d-f54f-4d7d-861f-fefe345554e6": "Year",
    "cms-d7fabe1e-d19b-4333-9eff-e80e0643f2fd": "YEAR",
    "cms-dgmq-aat3": "Fiscal Year",
    "cms-djen-97ju": "Processing Date",
    "cms-e3db6e56-149f-49ce-b374-40aecda2357b": "First_RBCS_Release_Year",
    "cms-eaed338b-847e-41b1-a4d3-a206f40dc72b": "YEAR",
    "cms-g6vv-u9sr": "Processing Date",
    "cms-ijh5-nb2v": "Processing Date",
    "cms-mj5m-pzi6": "Grd_yr",
    "cms-pudb-wetr": "Fiscal Year",
    "cms-qmdc-9999": "Processing Date",
    "cms-su9h-3pvj": "Fiscal Year",
    "cms-svdt-c123": "Processing Date",
    "cms-tbry-pc2d": "Processing Date",
    "cms-wue8-3vwe": "Year",
    "cms-xcdc-v8bm": "Processing Date",
    "cms-y2hd-n93e": "Processing Date",
    "cms-ypbt-wvdk": "Fiscal Year",
    "cms-yq43-i98g": "Fiscal Year",
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SET arrow_large_buffer_size=true;\nSELECT * FROM "{s.id}"',
        key=_KEY.get(s.id),
        temporal=_TEMPORAL.get(s.id),
    )
    for s in DOWNLOAD_SPECS
]
