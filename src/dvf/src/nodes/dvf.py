"""DVF — Demandes de Valeurs Foncières (French property transactions).

Single-corpus connector. The Etalab geo-dvf bulk distribution publishes the
whole corpus under https://files.data.gouv.fr/geo-dvf/latest/csv/ partitioned by
year -> departements/<dept>.csv.gz. Every partition file shares the SAME stable
40-column schema, so this is ONE catalog entity (`transactions`); year and
department are column values.

Fetch shape: stateless full re-pull (the default). The whole corpus is ~450MB
gzip across ~5 years x 97 departments and the `latest` tree is republished
wholesale ~twice a year, so re-fetching everything each run is cheap (a few
minutes) and picks up revisions/late corrections for free — no watermark, no
cursor. We DO batch the writes (one parquet per year+department) so no single
file is large enough to risk OOM and so files land small on R2; the batch files
glob-union back into the `dvf-transactions` view for the transform.

Raw is written close to source: measure columns typed (valeur_fonciere, areas,
counts, lat/long), everything else (ids, codes, dates, labels) kept as string to
preserve zero-padding and avoid parse failures. The transform does the final
typing/casting.
"""

import gzip
import io
import re

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

BASE = "https://files.data.gouv.fr/geo-dvf/latest/csv/"

# The stable geo-dvf CSV header (40 columns). Used to build the explicit type
# contract; a header drift surfaces downstream in the transform / tests.
COLUMNS = [
    "id_mutation", "date_mutation", "numero_disposition", "nature_mutation",
    "valeur_fonciere", "adresse_numero", "adresse_suffixe", "adresse_nom_voie",
    "adresse_code_voie", "code_postal", "code_commune", "nom_commune",
    "code_departement", "ancien_code_commune", "ancien_nom_commune",
    "id_parcelle", "ancien_id_parcelle", "numero_volume",
    "lot1_numero", "lot1_surface_carrez", "lot2_numero", "lot2_surface_carrez",
    "lot3_numero", "lot3_surface_carrez", "lot4_numero", "lot4_surface_carrez",
    "lot5_numero", "lot5_surface_carrez", "nombre_lots", "code_type_local",
    "type_local", "surface_reelle_bati", "nombre_pieces_principales",
    "code_nature_culture", "nature_culture", "code_nature_culture_speciale",
    "nature_culture_speciale", "surface_terrain", "longitude", "latitude",
]

_FLOAT_COLS = {
    "valeur_fonciere", "lot1_surface_carrez", "lot2_surface_carrez",
    "lot3_surface_carrez", "lot4_surface_carrez", "lot5_surface_carrez",
    "surface_reelle_bati", "surface_terrain", "longitude", "latitude",
}
_INT_COLS = {"nombre_lots", "nombre_pieces_principales"}


def _column_types() -> dict:
    types = {}
    for c in COLUMNS:
        if c in _FLOAT_COLS:
            types[c] = pa.float64()
        elif c in _INT_COLS:
            types[c] = pa.int64()
        else:
            types[c] = pa.string()
    return types


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _list_links(url: str, pattern: str) -> list:
    """Parse an nginx autoindex page for hrefs matching `pattern` (one capture group)."""
    html = _fetch_bytes(url).decode("utf-8", "replace")
    return sorted(set(re.findall(pattern, html)))


def fetch_transactions(node_id: str) -> None:
    asset = node_id  # "dvf-transactions"
    col_types = _column_types()
    convert = pacsv.ConvertOptions(column_types=col_types, include_columns=COLUMNS)

    years = _list_links(BASE, r'href="[^"]*?/(\d{4})/"')
    if len(years) < 3:
        raise AssertionError(f"expected >=3 years in geo-dvf index, got {years}")

    for year in years:
        dept_url = f"{BASE}{year}/departements/"
        depts = _list_links(dept_url, r'href="[^"]*?/([0-9AB]{2,3})\.csv\.gz"')
        if not depts:
            raise AssertionError(f"no department files found under {dept_url}")
        for dept in depts:
            raw = _fetch_bytes(f"{dept_url}{dept}.csv.gz")
            csv_bytes = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            table = pacsv.read_csv(io.BytesIO(csv_bytes), convert_options=convert)
            # batch_key is pure batch coordinate: <year>-<dept>
            save_raw_parquet(table, f"{asset}-{year}-{dept}")


DOWNLOAD_SPECS = [
    NodeSpec(id="dvf-transactions", fn=fetch_transactions, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="dvf-transactions-transform",
        deps=["dvf-transactions"],
        sql='''
            SELECT
                id_mutation,
                CAST(date_mutation AS DATE)              AS date_mutation,
                CAST(EXTRACT(year FROM CAST(date_mutation AS DATE)) AS INTEGER) AS year,
                numero_disposition,
                nature_mutation,
                CAST(valeur_fonciere AS DOUBLE)          AS valeur_fonciere,
                adresse_numero,
                adresse_suffixe,
                adresse_nom_voie,
                code_postal,
                code_commune,
                nom_commune,
                code_departement,
                id_parcelle,
                CAST(nombre_lots AS INTEGER)             AS nombre_lots,
                CAST(lot1_surface_carrez AS DOUBLE)      AS lot1_surface_carrez,
                code_type_local,
                type_local,
                CAST(surface_reelle_bati AS DOUBLE)      AS surface_reelle_bati,
                CAST(nombre_pieces_principales AS INTEGER) AS nombre_pieces_principales,
                code_nature_culture,
                nature_culture,
                CAST(surface_terrain AS DOUBLE)          AS surface_terrain,
                CAST(longitude AS DOUBLE)                AS longitude,
                CAST(latitude AS DOUBLE)                 AS latitude
            FROM "dvf-transactions"
            WHERE date_mutation IS NOT NULL
              AND id_mutation IS NOT NULL
        ''',
    ),
]
