"""ARCEP connector — French telecom/postal regulator open data.

Mechanism: the data.gouv.fr (uData/Etalab) REST API, organization
534fff58a3a7292c64a77cf6. Each rank-accepted subset is a schema *family* of CSV
resources within one dataset (collect grouped time/geo partitions that share a
schema). One generic `fetch_one` serves every node: it re-reads the org catalog,
selects the family's CSV resources by reproducing collect's family grouping
(so newly-published quarters are picked up automatically), downloads each,
parses it (cp1252 / ';' / preamble quirks handled in utils.parse_csv), tags each
row with its source resource title + partition period, and writes one
concatenated NDJSON raw asset. Values are kept as strings to preserve the source
faithfully across heterogeneous CSVs; the SQL transform publishes them 1:1.

Stateless full re-pull every run (the whole corpus is a few hundred MB at most,
fetchable in minutes) — no watermark/cursor. The maintain step gates cadence.
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_MAP
from utils import family_slug_of, parse_csv, decode_bytes, period_from_title

ORG_ID = "534fff58a3a7292c64a77cf6"
CATALOG_URL = (
    f"https://www.data.gouv.fr/api/1/datasets/?organization={ORG_ID}&page_size=200"
)
RESOURCE_URL = "https://www.data.gouv.fr/api/1/datasets/r/{rid}"


@transient_retry()
def _get(url: str, **kwargs):
    resp = get(url, timeout=(10.0, 300.0), **kwargs)
    resp.raise_for_status()
    return resp


def _dataset(slug: str) -> dict:
    catalog = _get(CATALOG_URL).json()
    for ds in catalog.get("data", []):
        if ds.get("slug") == slug:
            return ds
    raise AssertionError(f"dataset slug {slug!r} not found in ARCEP org catalog")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    spec = ENTITY_MAP[node_id]
    ds_slug = spec["dataset_slug"]
    fam_slug = spec["family_slug"]

    dataset = _dataset(ds_slug)
    members = [
        r
        for r in dataset.get("resources", [])
        if (r.get("format") or "").lower() == "csv"
        and family_slug_of(r.get("title") or "", ds_slug) == fam_slug
    ]
    if not members:
        raise AssertionError(
            f"{node_id}: no CSV resources matched family {fam_slug!r} in {ds_slug!r}"
        )

    rows: list[dict] = []
    for res in members:
        url = RESOURCE_URL.format(rid=res["id"])
        content = _get(url).content
        records = parse_csv(decode_bytes(content))
        title = res.get("title") or ""
        period = period_from_title(title)
        for rec in records:
            rec["_resource_title"] = title
            rec["_period"] = period
        rows.extend(records)

    if not rows:
        raise AssertionError(f"{node_id}: parsed 0 rows from {len(members)} resource(s)")

    # Resources within a family can carry different columns across quarters
    # (e.g. a `percent_area` field added in later releases). DuckDB's
    # read_json_auto infers the schema from a leading sample of the NDJSON and
    # then errors on any later row bearing an unsampled key. Normalize every row
    # to the union of keys (insertion-ordered, missing filled with None) so the
    # raw NDJSON has one homogeneous schema and the pass-through transform reads
    # cleanly regardless of sample size.
    all_keys: dict[str, None] = {}
    for rec in rows:
        all_keys.update(dict.fromkeys(rec))
    rows = [{k: rec.get(k) for k in all_keys} for rec in rows]

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in ENTITY_MAP
]


# Per-subset grain declarations, keyed by download/spec id. Values are
# (key, temporal) on OUTPUT columns of the pass-through SELECT *. `_period` is the
# connector-tagged partition period (always populated for every row). Keys are
# declared only where uniqueness is well supported; the schema-drifting
# new-deal-mobile inventories (columns renamed across quarters) and the
# period-concatenated geographic panels are left keyless.
_GRAIN = {
    # FTTH national quality time series — one row per date.
    "arcep-qualite-des-reseaux-en-fibre-optique--historique-des-indicateurs-de-qualite-ftth-au-niveau-national": (
        ("date",), "date",
    ),
    # FTTH quality by parent operator — one row per (date, parent).
    "arcep-qualite-des-reseaux-en-fibre-optique--historique-des-indicateurs-de-qualite-ftth-par-maison-mere": (
        ("date", "maison_mere"), "date",
    ),
    # MCC/MNC/IMSI code registry — one row per assigned code.
    "arcep-ressources-en-numerotation-telephonique--majmnc-liste-des-codes-mcc-mnc-imsi-attribues": (
        ("mcc_mnc",), "date_attribution",
    ),
    # MAJNUM number-block registry — one row per prefix (ezabpqm).
    "arcep-ressources-en-numerotation-telephonique--majnum-liste-des-ressources-en-numerotation-telephoniques-attribuees": (
        ("ezabpqm",), "date_attribution",
    ),
    # MAJPORTA routing-prefix registry — one row per prefix.
    "arcep-ressources-en-numerotation-telephonique--majporta-liste-des-prefixes-de-routage": (
        ("ezabpqm",), "date_attribution",
    ),
    # IPv6 adoption — one row per (country, date).
    "arcep-statistiques-ipv6--data-ipv6": (
        ("iso", "date"), "date",
    ),
    # Temporal-only (grain uncertain / period-concatenated / schema-drifting).
    "arcep-le-marche-du-haut-et-tres-haut-debit-fixe-deploiements--releve-geographique-donnees-sous-jacentes": (
        None, "date_fin_dep",
    ),
    "arcep-qualite-des-reseaux-en-fibre-optique--historique-des-indicateurs-de-qualite-de-realisation-des-raccordements-et-de-delais-de-reprise-des-malfacons": (
        None, "_period",
    ),
    "arcep-qualite-des-reseaux-en-fibre-optique--indicateurs-de-qualite-ftth-par-reseau": (
        None, "_period",
    ),
    "arcep-sites-indisponibles--sites-indisponibles": (None, "date"),
    "arcep-tableau-bord-du-new-deal-mobile--indicateurs-couverture-4g": (None, "trimestre"),
    "arcep-tableau-bord-du-new-deal-mobile--liste-sites-operateurs-mobiles": (None, "_period"),
    "arcep-tableau-bord-du-new-deal-mobile--metropole-sites": (
        None, "date_ouverturecommerciale_5g",
    ),
}


# Each subset is published 1:1 from its raw family asset. The transform is a thin
# pass-through: DuckDB reads the NDJSON (union of columns across the family's
# resources) and publishes it. Empty result = node failure by design.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        key=_GRAIN.get(s.id, (None, None))[0],
        temporal=_GRAIN.get(s.id, (None, None))[1],
    )
    for s in DOWNLOAD_SPECS
]
