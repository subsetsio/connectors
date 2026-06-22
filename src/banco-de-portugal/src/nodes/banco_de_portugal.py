"""Banco de Portugal (BPstat) connector.

Source: BPstat Data API v1 (https://bpstat.bportugal.pt/data/v1/), the official
open-data API of Banco de Portugal. No auth, no registration.

Shape: catalog connector. One download spec per BPstat *dataset* (143 rank-active
datasets). Each dataset is a statistical hypercube whose observations are served
as JSON-stat v2.0. A dataset is fetched by paginating its series:
  GET /domains/{domain_id}/datasets/{dataset_id}/?lang=EN&page=N&page_size=100
page_size is capped at 100 by the API; pages enumerate the dataset's series.
Each page returns a JSON-stat cube covering that page's series. We decode every
series' observations directly from its dimension-category coordinates (lossless;
the per-page cube grid can enclose cells belonging to series listed on *other*
pages, so we never trust the raw cell count — we extract exactly this page's
series and let the other cells be captured on their own page).

Published as long-format time series, one Delta table per dataset:
  (reference_date, series_id, series_label, value).

Fetch strategy: stateless full re-pull. The whole corpus is ~39k series /
low-millions of observations and re-fetches in minutes; the API exposes an
`obs_since` filter but we deliberately do a full pull each refresh so revisions
and late corrections are always picked up. Raw is streamed to gzipped NDJSON so
the largest datasets (up to ~6.4k series) never materialise fully in memory.
"""
import json

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_writer

BASE = "https://bpstat.bportugal.pt/data/v1"
# page_size is capped at 100 by the API, but for datasets with large hypercubes
# the server 502s while computing a 100-series page (deterministic, reproducible
# with zero load). The cube cost varies per dataset, so we start large and shrink
# on a persistent server error — restarting that dataset's pagination cleanly so
# page boundaries stay consistent for the working size.
# The ladder must descend BELOW the smallest datasets' series counts: pages
# enumerate *series*, so a dataset with only N series returns its entire cube on
# one page for any page_size >= N (shrinking 100->5 does nothing for it). Some
# datasets have very few series but thousands of dates (e.g. domain 29's
# 23e0cdd5... is 4 series x 3016 dates -> a single 2.9MB cube the server drops
# under concurrent load); only page_size 2/1 actually splits it into the small
# (~160KB) pages that survive. page_size=1 caps at MAX_PAGES series per dataset.
PAGE_SIZES = [100, 50, 25, 10, 5, 2, 1]
MAX_PAGES = 5000         # safety ceiling; raises if hit (catches runaway growth)

from constants import ENTITY_IDS

DATASET_DOMAIN = {
    "002abf63d5a4efb3e35ab5321251d7c5": 9,
    "00ac0311f09ecac48b82a9d92f8aa462": 8,
    "023d7ab3054d8a0d2db8de50c0ca394b": 209,
    "02f01a0adab4928e0844d12d6d068a75": 49,
    "05e2845d5d567afd88b699a91b0c20b8": 3,
    "0623eb9d3bebc56c07359ba1fa875039": 181,
    "073a8bb09c3da76f5a75545464c0ba76": 4,
    "07d36f662cea4b19f4b2c2cf5435771d": 21,
    "08adcab6f448ae4408de0cca87b4cb4c": 18,
    "08b8569381865912db2e7613e889ff06": 162,
    "08ea9a8e70896fd8c1fd3b99d71c7dc4": 4,
    "0da378eb4c39011fb7fb371c6623af8f": 19,
    "10470e6b60c710218dd2a0e6a20fb040": 28,
    "11efc3f8b69ac058c7f6409af360ea6d": 19,
    "14ed8f5141827c03e802bdcb99bf1ad8": 178,
    "188848bcf570a3be11b08cc46eb88f6d": 161,
    "1a2b849de5d914ee33be7d126408f341": 194,
    "1d7bcbd5ff6e9762ecd7d1febdd435f7": 19,
    "1e2c4732d70e81e931db92220ba4e54b": 170,
    "1fd18ec0fbb9e880647ea3978ec84bc9": 19,
    "2034ce19b02f58f035f8cb566fe07d7a": 4,
    "215ab4b322f0f6003e20dcf5adf0efdb": 8,
    "21cb465ad0c9ddb3fccf5260e4f289e8": 55,
    "22394483d575a2ff580e98f45939476b": 13,
    "226fdb00077f154289f54e87da9e68dc": 189,
    "228747b58996ea7eb475aef69800cfb1": 32,
    "23e0cdd56bddb4ad3016a9c3ad63a539": 29,
    "2829cb9155cb4f6ba6906db6b204c4bc": 22,
    "28b6a921e1a4a9e326e724ab3e043d97": 19,
    "29bea6a6e6f5f7e750ff7ff615ef8d6e": 3,
    "2d8f1e2983223b37ab0ec0130fdc49d8": 8,
    "2eb6c5abd0c5183aa083bc53e7f2e270": 53,
    "332441c9d65de71a0c842ac6496c1ee2": 168,
    "348f0a09f36f47c5eef24187b4b4afaa": 204,
    "34e4f2e4ddae13cba3e74c926fc23f48": 53,
    "35da7b3f137ea2fd15e7ae82db8ae966": 6,
    "36a06e0b7d0f57014851b37e204234cc": 3,
    "3704e631f08f5b892fd8bcf7f6322370": 19,
    "38e88a535eeea89658833a205360e74e": 4,
    "38fa260d12e2d0c4f648fe3e6eabccf8": 19,
    "3a876705f69e7a8775ca98a6510d685d": 45,
    "3d9b94e365f16dae943a1a560da7de22": 13,
    "3f1cfafc23078c774aee14c4d084a84d": 50,
    "40f2813d87e190be02f9e18e927fadf0": 9,
    "417a62cea5735f7af3903ab9081ae6aa": 30,
    "455e4f563c520ceb9aa65908625d44ec": 41,
    "45d4559c8aafd8d644b339ab7488e237": 19,
    "471186a839daf97d9280419fc06c8579": 22,
    "48301d7699f7573d40c53634d911ffcb": 19,
    "4900a7b66f6890857b1eeb2edb1e1148": 128,
    "49b3817438d5e78c2f875e029f89366b": 6,
    "4b3f09fa9a32fe920622db20d6b673a5": 8,
    "4c4e01bce4a325307e95143e099a1a50": 3,
    "4d73fa9f4befd82d7aa1d75debd79bd2": 28,
    "504020fd408fb738203d951de83f18d3": 20,
    "5128cfe1c89da8cca3b74288e5ceced7": 8,
    "543e60d9f59c28f40aea200d1871f7fa": 19,
    "54537a5f2b6138f33c54cff2753ee1cc": 5,
    "551ffd50a03df1e822e8841a83130e46": 207,
    "55ead4192827e5e6e356bf0246b83467": 172,
    "561baccbc4f3ea9c300d706f30e98fed": 8,
    "56ebacd8518e60ef58c85cb8185b4818": 18,
    "5bb7a39ed6b4e4f925656b453e81174b": 36,
    "5e42e78146bb44759188678266b04c4e": 21,
    "5f91d75d7d2c5ed3a7dbe1c3316f5489": 8,
    "61f3b38efb7ed30c5595f0211fb10344": 27,
    "626d05f424a651dac45b8f81f6150ffd": 169,
    "63e8780cdb0c94c323528c7237b7a4b8": 186,
    "659a3864b75ae68c437cfe5669fa2fac": 170,
    "690b7b36fd36c0dbe249c48cbbc39524": 26,
    "6a83b46f5911d1b086a2891746a2fd9a": 186,
    "6d2cc2aad985abe4db42b9d1f83c8c97": 3,
    "6eaa8db94523f54733dddc22479c11a4": 21,
    "76b3cae4c8fc3a305f7780c2390e70e7": 5,
    "778bb430910438b4d74abec51d81a195": 41,
    "78c68c0b89096b4308de694415bd4a48": 13,
    "7962dd30f627940482e2c85f8bfaca84": 13,
    "7c204b15014887c6f0321f7553e5dcd6": 8,
    "7cf167b0b4012c66fd9de53d8420413a": 36,
    "7d183dbe8c9582e633ed1f2e10c838cf": 58,
    "7d87ed3ee74d4fa55adc86427fddf086": 24,
    "7e72982e9cfa35e3887bbd26332621e4": 36,
    "7f13efcd65fc6bd0c5adb0e8d29d9b44": 41,
    "83489eb2e300881d87b13ff5187e5654": 28,
    "851facff504532e95cf096ca9c6a8b9a": 21,
    "85c2d956038233432ce61f230f7dddab": 186,
    "869da7cdeba8cab9c8b347f3107726d7": 8,
    "8719b182e15adb23bf5058b90586199c": 45,
    "87df50d4fc441cabd72f6e964c4a2748": 23,
    "8a9766347128321e0bd8a7806d8d2c02": 54,
    "8b6aeea21d8686f3788d49c7551779df": 54,
    "8f63e6ad2187cfe41cf8e436b4191c93": 5,
    "8f81a135c26dd5e58fd92232e266e951": 178,
    "90cc8b36009d0c497d3c7375b57506ac": 13,
    "911c96b897efe17121383bc621c3966e": 31,
    "91addfddec26842bcb83f8f31d91b64e": 13,
    "921a2108733e34fe71b5fed3dfa75c20": 18,
    "932d2d9ee44b584407c3294484d26420": 27,
    "93441ab6408be15acced35b8ed98cd97": 38,
    "93f7abcc89d67adcc702dceffdcded71": 131,
    "961306c1ed49daf795a53dc5fea4a04b": 188,
    "97242b6ccad817b22b9016cd9fd82f32": 53,
    "9744c7a78f7417d4a91cf1a1b55fac1d": 21,
    "981c85593e50ea948ec3f67c63c4898f": 8,
    "9a04dd6b16441184dd993a5015490e72": 10,
    "9ab0b6dd481ff9d0a79aeca89363b9ec": 21,
    "a654b37e97983a826eb9f4f399c0bb14": 28,
    "a95fb8eb257a889fb18ee775e91c7adf": 209,
    "aea9d7f70ddf9c6de29feaeba86a9456": 50,
    "b57d7d3c318057c5c9e43b5e4671e4ae": 18,
    "b8cc662879c9f7b0f3faf89c7871fc38": 59,
    "bbee05085d21f58e4dac4432dc205060": 49,
    "bffd128b51687c436e6aaba2dbf91f83": 163,
    "c1a38fb2d603b1a667350319b16d241c": 49,
    "c4db40b75370917aaf045d1cff74c142": 21,
    "c95282a6e897efdc36832d5611fac100": 13,
    "cbddec4e002dfdf47d22797214f1e3ff": 24,
    "ce3e4e50cda325537eff729ef64037cd": 54,
    "d0b1b2758e974a808f5e424d151b13df": 28,
    "d45bb68e792a6b1b2fc36d6a90da4f20": 186,
    "d5681b663fe52e02cad86e184e89fef5": 13,
    "d5bf6198a39f1e77b0d14dda97103de0": 206,
    "d64e4ec9e100e1eb22e7eeb21a298d09": 28,
    "d783a87bce2d7f1c05dd9c052d6d2588": 27,
    "da133c091337a417b8b242c65e477ca0": 59,
    "db00d7f05e0e77793a31d96f70604270": 51,
    "db0366b1f32fc6842a7541885fcb5600": 55,
    "e102f689e64dc35ddcbb298713e864ce": 203,
    "e1bc26e910f42ba278827b0ad804be2a": 139,
    "e2bc3b33d169f2d0885cffb9183fb48e": 28,
    "eb8297d3228914244941876881cf5d97": 27,
    "ec3a02a9e24bff60450cf98b6b094709": 49,
    "ec7b2a0f066656833f1013b3a2f9f189": 21,
    "ed2ee8fa340b39506d9341e5ed17afbb": 49,
    "f4eb37c104671b320d17e4a31477844a": 28,
    "f648a7e7dec2e61dd4bdd6ba56ac519b": 21,
    "f773d814da50caa6a60bb5c4ec672077": 26,
    "f7f01aff8e7ae07ad0de335346169aed": 179,
    "f8d9de1f6eafa76afc24ab71b570bf4c": 181,
    "fd4ee68152d08080b696ee7b7071ccf5": 5,
    "fd8f42946d3f4c45c144e9d62065dc72": 41,
    "fda75fd8c8a2549df8431ac9fd5fb0fc": 23,
    "ff99fb59e7ab2b6801a86a2e089721dc": 169,
}

_TRANSIENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # Retry only genuinely transient HTTP conditions: rate-limiting (429)
        # and "service unavailable" (503). We deliberately do NOT retry
        # 500/502/504 here: for this API those are overwhelmingly the
        # deterministic "cube too big -> the server computes then bails" failure,
        # whose correct fix is a SMALLER page (handled by fetch_one's shrink
        # loop), not the same oversized request again. Retrying them five times
        # at the same page_size just burns ~5x the backoff and pile-drives an
        # already-struggling server with expensive doomed cube computations —
        # the dynamic that cascaded into a server-wide 502 storm on the
        # 2026-06-18 run (5 large datasets each spent ~286s exhausting retries
        # at page_size=100 before they could even start shrinking). Shrinking on
        # the first 5xx both recovers faster and cuts our load on the API ~5x. A
        # truly transient 500/502/504 just costs one cheap permanent step down to
        # a smaller page_size for this refresh.
        return code in (429, 503)
    return False


# Randomised backoff so the parallel nodes de-synchronise instead of retrying in
# lockstep (a fixed schedule has every node hammer the server at the same
# instants). This handles genuinely transient blips; deterministic
# "cube too big -> 502" failures are handled by shrinking page_size in fetch_one.
@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(5),
    wait=wait_random_exponential(multiplier=1, max=30),
    reraise=True,
)
def _fetch_page(domain_id: int, dataset_id: str, page: int, page_size: int) -> dict:
    resp = get(
        f"{BASE}/domains/{domain_id}/datasets/{dataset_id}/",
        params={"lang": "EN", "page": page, "page_size": page_size},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def _parse_page(d: dict):
    """Yield (series_id, series_label, reference_date, value) for every
    observation of the series listed on THIS JSON-stat page.

    The cube is row-major over `id` (dimension order) with sizes `size`; the
    flat value array is dense (list) or sparse ({index: value}). We compute each
    series' base offset from its dimension-category coordinates and walk the
    reference_date axis, so assignment of cell -> series is exact.
    """
    ids = d["id"]
    size = d["size"]
    dim = d["dimension"]
    value = d["value"]
    ndim = len(ids)

    strides = [1] * ndim
    for i in range(ndim - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]

    rd_pos = ids.index("reference_date")
    rd_stride = strides[rd_pos]
    date_index = dim["reference_date"]["category"]["index"]

    # per non-date dimension: category_id(int) -> position, and that dim's stride
    cat_pos = {}
    dim_stride = {}
    for i, did in enumerate(ids):
        if did == "reference_date":
            continue
        cat_pos[did] = {
            int(c): p for p, c in enumerate(dim[did]["category"]["index"])
        }
        dim_stride[did] = strides[i]

    if isinstance(value, dict):
        def getv(k):
            return value.get(str(k))
    else:
        vlen = len(value)

        def getv(k):
            return value[k] if 0 <= k < vlen else None

    for s in d["extension"]["series"]:
        cats = {
            int(dc["dimension_id"]): int(dc["category_id"])
            for dc in s["dimension_category"]
        }
        base = 0
        for did in cat_pos:
            base += cat_pos[did][cats[int(did)]] * dim_stride[did]
        sid = s["id"]
        label = s.get("label") or str(sid)
        for j, date in enumerate(date_index):
            v = getv(base + j * rd_stride)
            if v is None:
                continue
            yield sid, label, date, v


def _crawl_dataset(domain_id, dataset_id, page_size, f):
    """Paginate the whole dataset at a fixed page_size, streaming rows to f.
    Raises the underlying httpx error if a page can't be fetched."""
    page = 1
    while True:
        d = _fetch_page(domain_id, dataset_id, page, page_size)
        series = d.get("extension", {}).get("series", [])
        n = len(series)
        if n == 0:
            break
        for sid, label, date, val in _parse_page(d):
            f.write(
                json.dumps(
                    {
                        "series_id": sid,
                        "series_label": label,
                        "reference_date": date,
                        "value": val,
                    }
                )
                + "\n"
            )
        if n < page_size:
            break  # last (partial) page
        page += 1
        if page > MAX_PAGES:
            raise RuntimeError(
                f"banco-de-portugal-{dataset_id}: exceeded MAX_PAGES={MAX_PAGES} "
                "safety cap (dataset larger than expected — raise the ceiling)"
            )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = node_id[len("banco-de-portugal-"):]
    domain_id = DATASET_DOMAIN[dataset_id]

    last_err = None
    for i, page_size in enumerate(PAGE_SIZES):
        try:
            # "wt" truncates, so a restart at a smaller page_size cleanly
            # overwrites any partial content from a failed larger-size attempt.
            with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
                _crawl_dataset(domain_id, dataset_id, page_size, f)
            return
        except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
            # Two manifestations of the same "cube too big under load" failure:
            #  - a 5xx (server computes the page, then bails), and
            #  - an empty / non-JSON 200 body (server gives up and returns nothing,
            #    so resp.json() raises JSONDecodeError). Both recover the same way:
            # shrink page_size and restart the dataset, rather than retrying the
            # same oversized request (which just re-triggers the same drop and
            # piles load on an already-struggling server — see _is_transient).
            shrinkable = isinstance(e, json.JSONDecodeError) or (
                e.response.status_code in (500, 502, 503, 504)
            )
            if shrinkable and i + 1 < len(PAGE_SIZES):
                last_err = e
                reason = "empty/non-JSON body" if isinstance(
                    e, json.JSONDecodeError
                ) else f"HTTP {e.response.status_code}"
                print(
                    f"{asset}: {reason} at page_size={page_size}; "
                    f"retrying whole dataset at page_size={PAGE_SIZES[i + 1]}"
                )
                continue
            raise
    raise last_err  # exhausted every page_size


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"banco-de-portugal-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(reference_date AS DATE)  AS reference_date,
                CAST(series_id AS BIGINT)     AS series_id,
                series_label,
                CAST(value AS DOUBLE)         AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
