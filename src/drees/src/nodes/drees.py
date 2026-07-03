"""DREES (Direction de la recherche, des etudes, de l'evaluation et des
statistiques) — French health & social-affairs statistics.

Mechanism: Opendatasoft Explore API v2.1 at
https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1. Each rank-accepted
dataset is fetched in full from its stable per-entity parquet export
(/catalog/datasets/{dataset_id}/exports/parquet), which streams the entire table
in one request — no auth, no pagination. Fetch shape is the default stateless
full re-pull: every run overwrites each raw asset with a complete snapshot, so
DREES's annual revisions are picked up for free. The corpus is ~47 datasets,
each a few rows to ~1.2M; the whole pull is minutes and cents.

Each subset's transform is a straight typed passthrough — the ODS parquet export
already carries clean snake_case columns and proper types, so there is no shared
schema across the heterogeneous portal to normalise to.
"""
import io

import pyarrow.parquet as pq

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS

BASE = "https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1"

# spec.id is f"drees-{eid.lower().replace('_','-')}", which is NOT reversible
# back to the upstream dataset_id (case + underscores are lost). Keep the exact
# mapping so fetch_one can rebuild the export URL from the node id it's handed.
SPEC_TO_DATASET = {
    f"drees-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}
assert len(SPEC_TO_DATASET) == len(ENTITY_IDS), "spec id collision in ENTITY_IDS"


@transient_retry()  # 6 attempts, exponential 4..120s backoff, reraise on exhaust
def _fetch_parquet(dataset_id: str) -> bytes:
    url = f"{BASE}/catalog/datasets/{dataset_id}/exports/parquet"
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()  # inside the retry so 5xx/429 are retried
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = SPEC_TO_DATASET[node_id]
    content = _fetch_parquet(dataset_id)
    table = pq.read_table(io.BytesIO(content))
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"drees-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Per-dataset primary observation-period column (freshness axis). The portal is
# heterogeneous so the time column's name varies (annee / date / a cohort year);
# datasets absent here are genuinely timeless reference/microdata tables. This is
# purely declarative metadata — it never affects the passthrough SQL.
_TEMPORAL = {
    'drees-305-les-comptes-de-la-protection-sociale': 'annee',
    'drees-596-enfance-et-jeunesse-en-danger': 'annee',
    'drees-601-indicateurs-de-contexte': 'annee',
    'drees-619-indicateurs-financiers': 'annee',
    'drees-627-personnes-en-situation-de-handicap': 'annee',
    'drees-631-insertion-sociale-et-minima-sociaux': 'annee',
    'drees-639-personnes-agees': 'annee',
    'drees-beneficiaires-apa-a-domicile-base-floutee-v1': 'dateeval_apa_flou',
    'drees-cns-financement': 'annee',
    'drees-cns-sha': 'annee',
    'drees-composition-des-revenus-des-menages-juste-avant-et-juste-apres-le-depart-a-la-retraite': 'premiere_annee_pleine_de_retraite',
    'drees-comptes-de-la-sante-partage-volume-prix': 'annee',
    'drees-covid-19-resultats-issus-des-appariements-entre-si-vic-si-dep-et-vac-si': 'date',
    'drees-covid-19-resultats-par-age-issus-des-appariements-entre-si-vic-si-dep-et-vac-si': 'date',
    'drees-covid-19-resultats-regionaux-issus-des-appariements-entre-si-vic-si-dep-et-vac-s': 'date',
    'drees-departretraite-et-incapacite': 'annee',
    'drees-departretraite-parcsp': 'annee',
    'drees-depenses-de-sante-et-restes-a-charge': 'annee',
    'drees-drees-projections-infirmieres-2024': 'annee',
    'drees-effectifs-salaries-hospitaliers-series-longues': 'annee',
    'drees-enquete-oc-depuis-2019': 'annee',
    'drees-fichier-maternites-112021': 'annee',
    'drees-invalidite-pensmoy-dd': 'annee',
    'drees-lits-de-reanimation-de-soins-intensifs-et-de-surveillance-continue-en-france0': 'annee',
    'drees-ods-revenu-liberal-des-medecins-liberaux-prod2022': 'annee',
    'drees-organismes-complementaires-comptes-detailles': 'annee',
    'drees-patients-hospitalises-pour-gestes-auto-infliges-depuis-2012': 'annee',
    'drees-rec01': 'annee',
    'drees-rec02': 'annee',
    'drees-rec03': 'annee',
    'drees-rec04': 'annee',
    'drees-rec05': 'annee',
    'drees-rec06': 'annee',
    'drees-rec07': 'annee',
    'drees-rec08': 'annee',
    'drees-rec09': 'annee',
    'drees-repartition-des-taux-de-remplacement-entre-les-revenus-juste-avant-et-juste-apres-la-retraite': 'premiere_annee_pleine_de_retraite',
    'drees-repartition-par-categorie-de-niveau-de-vie-juste-avant-et-juste-apres-le-depart-a-la-retraite': 'premiere_annee_pleine_de_retraite',
    'drees-series-longues-passages-urgences-2017-2023': 'date',
    'drees-skyline': 'annee',
    'drees-trajectoires-des-beneficiaires-de-minima-sociaux': 'annee',
}

# One published Delta table per dataset. The ODS parquet already has clean types
# and column names, so the transform is a passthrough that simply re-publishes
# the snapshot (and acts as the 0-rows correctness gate).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        **({"temporal": _TEMPORAL[s.id]} if s.id in _TEMPORAL else {}),
    )
    for s in DOWNLOAD_SPECS
]
