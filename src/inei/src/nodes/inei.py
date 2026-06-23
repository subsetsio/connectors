"""INEI (Peru) -- SIRTOD national statistical time-series.

Source: the SIRTOD JSON backend at https://systems.inei.gob.pe/SIRTOD/app/consulta/
(reverse-engineered from the app JS; see research). All endpoints are POST and
return text/plain ISO-8859-1 JSON arrays. There is NO bulk export, but the data
endpoints accept a comma-joined ``indicador_listado``, so we batch many
indicators per request instead of one call per series.

Three published tables:
  inei-indicators     -- indicator catalog / taxonomy (reference, joinable)
  inei-values-annual  -- long-format annual national observations
  inei-values-monthly -- monthly national observations (source returns 12 wide
                         month columns per year; the transform melts to long)

Fetch shape: stateless full re-pull every run (shape 1). The whole corpus is
~6900 national indicators and re-pulls in a few minutes / a couple hundred
batched POSTs. fecha_modificacion exposes only ONE global timestamp -- there is
no usable per-series incremental filter -- so a full re-pull is correct and picks
up revisions/late corrections for free. National level only (tipo_ubigeo=0);
subnational levels require ubigeo enumeration and are out of scope.
"""
import datetime
import json

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    post,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://systems.inei.gob.pe/SIRTOD/app/consulta"
BATCH_SIZE = 50              # indicators per data request (comma-joined)
ANIO_DESDE = "1900"         # query floor; the real start is whatever the source returns
TIMEOUT = (10.0, 180.0)     # (connect, read)
# INEI encodes "no data" with magic NA codes: -9999999999.99999 and -8888888888.88888.
# The transforms drop rows whose value falls in a narrow band around either code
# (precise bands, so legitimate large negatives -- e.g. trade balances -- survive).
_SENTINEL_FILTER = (
    "value NOT BETWEEN -10000000000.0 AND -9999999999.0 "
    "AND value NOT BETWEEN -8888888889.0 AND -8888888888.0"
)


@transient_retry()
def _post(endpoint: str, data: dict | None = None):
    """POST one SIRTOD endpoint and return parsed JSON (or None for empty/null)."""
    resp = post(f"{BASE}/{endpoint}", data=data or {}, timeout=TIMEOUT)
    resp.raise_for_status()  # inside the retry: 5xx/429 become transient
    text = resp.text.strip()
    if not text or text == "null":
        return None
    return json.loads(text)


def _anio_hasta() -> str:
    # Discover the upper bound from the clock (INEI publishes population
    # projections beyond the current year, so leave generous headroom).
    return str(datetime.date.today().year + 1)


def _batched(seq: list, n: int):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _load_tree() -> tuple[list[dict], dict[str, dict]]:
    """Fetch the thematic tree; return (indicator leaves, folder-by-idTema)."""
    tree = _post("arboltematico")
    if not tree:
        raise RuntimeError("arboltematico returned no data")
    folders = {n["idTema"]: n for n in tree if n.get("tipo") == "folder"}
    leaves = [
        n
        for n in tree
        if n.get("tipo") != "folder" and n.get("codigoIndicador")
    ]
    return leaves, folders


def _theme_path(leaf: dict, folders: dict[str, dict]) -> tuple[str | None, str | None]:
    """Resolve a leaf's immediate parent folder name and its top-level theme."""
    parent = folders.get(leaf.get("idPadre"))
    immediate = (parent.get("nombreTema") or "").strip() or None if parent else None
    # Climb idPadre to the highest resolvable folder. The tree has two hierarchies:
    # the main one roots at the synthetic "1", a second (census) one roots at a node
    # that isn't tagged as a folder -- so we stop at the last folder we can resolve
    # rather than discarding the whole chain.
    root = parent
    guard = 0
    while root and guard < 50:
        pid = root.get("idPadre")
        if pid in (None, "", "1"):
            break
        nxt = folders.get(pid)
        if nxt is None:
            break
        root = nxt
        guard += 1
    root_name = (root.get("nombreTema") or "").strip() or None if root else None
    return immediate, root_name


def _to_float(v):
    if v is None or v == "":
        return None
    return float(v)


# --------------------------------------------------------------------------- #
# inei-indicators -- indicator catalog / taxonomy
# --------------------------------------------------------------------------- #
INDICATOR_SCHEMA = pa.schema(
    [
        ("codigo_indicador", pa.int64()),
        ("nombre_indicador", pa.string()),
        ("nombre_indicador_en", pa.string()),
        ("tema", pa.string()),
        ("tema_raiz", pa.string()),
        ("id_tema", pa.int64()),
        ("id_padre", pa.int64()),
        ("ambito_departamental", pa.bool_()),
        ("ambito_provincial", pa.bool_()),
        ("ambito_distrital", pa.bool_()),
    ]
)


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    leaves, folders = _load_tree()
    rows = []
    for lf in leaves:
        immediate, root = _theme_path(lf, folders)
        rows.append(
            {
                "codigo_indicador": int(lf["codigoIndicador"]),
                "nombre_indicador": (lf.get("nombreIndicador") or "").strip() or None,
                "nombre_indicador_en": (lf.get("nombreIndicadorIngles") or "").strip()
                or None,
                "tema": immediate,
                "tema_raiz": root,
                "id_tema": int(lf["idTema"]) if lf.get("idTema") else None,
                "id_padre": int(lf["idPadre"]) if lf.get("idPadre") else None,
                "ambito_departamental": lf.get("departamentos") == "1",
                "ambito_provincial": lf.get("provincias") == "1",
                "ambito_distrital": lf.get("distritos1") == "1",
            }
        )
    table = pa.Table.from_pylist(rows, schema=INDICATOR_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# inei-values-annual -- long-format annual national observations
# --------------------------------------------------------------------------- #
ANNUAL_SCHEMA = pa.schema(
    [
        ("indicador_id", pa.int64()),
        ("anio", pa.int64()),
        ("valor", pa.float64()),
        ("valor2", pa.float64()),
    ]
)


def fetch_values_annual(node_id: str) -> None:
    asset = node_id
    leaves, _ = _load_tree()
    ids = [lf["codigoIndicador"] for lf in leaves]
    hasta = _anio_hasta()
    rows = []
    for batch in _batched(ids, BATCH_SIZE):
        data = _post(
            "dato_anual",
            {
                "indicador_listado": ",".join(batch),
                "tipo_ubigeo": "0",  # national total -- omit ubigeo_listado
                "anio_desde": ANIO_DESDE,
                "anio_hasta": hasta,
            },
        )
        if not data:
            continue
        for r in data:
            rows.append(
                {
                    "indicador_id": int(r["indicadorId"]),
                    "anio": int(r["anioIntervalo"]),
                    "valor": _to_float(r.get("datoAnual")),
                    "valor2": _to_float(r.get("datoAnual2")),
                }
            )
    table = pa.Table.from_pylist(rows, schema=ANNUAL_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# inei-values-monthly -- wide monthly national observations (melted in transform)
# --------------------------------------------------------------------------- #
MONTHLY_SCHEMA = pa.schema(
    [("indicador_id", pa.int64()), ("anio", pa.int64())]
    + [(f"m{m}", pa.float64()) for m in range(1, 13)]
)


def fetch_values_monthly(node_id: str) -> None:
    asset = node_id
    leaves, _ = _load_tree()
    ids = [lf["codigoIndicador"] for lf in leaves]
    hasta = _anio_hasta()
    rows = []
    for batch in _batched(ids, BATCH_SIZE):
        data = _post(
            "dato_mensual",
            {
                "indicador_listado": ",".join(batch),
                "tipo_ubigeo": "0",
                "anio_desde": ANIO_DESDE,
                "anio_hasta": hasta,
            },
        )
        if not data:
            continue  # annual-only indicators return [] here
        for r in data:
            row = {
                "indicador_id": int(r["indicadorId"]),
                "anio": int(r["anioIntervalo"]),
            }
            for m in range(1, 13):
                row[f"m{m}"] = _to_float(r.get(f"datoMensual{m}"))
            rows.append(row)
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="inei-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="inei-values-annual", fn=fetch_values_annual, kind="download"),
    NodeSpec(id="inei-values-monthly", fn=fetch_values_monthly, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="inei-indicators-transform",
        deps=["inei-indicators"],
        sql="""
            SELECT
                codigo_indicador,
                nombre_indicador,
                nombre_indicador_en,
                tema,
                tema_raiz,
                ambito_departamental,
                ambito_provincial,
                ambito_distrital
            FROM "inei-indicators"
            WHERE codigo_indicador IS NOT NULL
              AND nombre_indicador IS NOT NULL
        """,
    ),
    SqlNodeSpec(
        id="inei-values-annual-transform",
        deps=["inei-values-annual"],
        sql=f"""
            SELECT indicador_id, anio AS year, value
            FROM (
                SELECT indicador_id, anio, valor AS value
                FROM "inei-values-annual"
            ) AS a
            WHERE value IS NOT NULL
              AND anio IS NOT NULL
              AND {_SENTINEL_FILTER}
        """,
    ),
    SqlNodeSpec(
        id="inei-values-monthly-transform",
        deps=["inei-values-monthly"],
        sql=f"""
            SELECT
                indicador_id,
                anio AS year,
                CAST(SUBSTR(month_col, 2) AS INTEGER) AS month,
                make_date(anio, CAST(SUBSTR(month_col, 2) AS INTEGER), 1) AS date,
                value
            FROM (
                UNPIVOT "inei-values-monthly"
                ON m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12
                INTO NAME month_col VALUE value
            ) AS u
            WHERE value IS NOT NULL
              AND {_SENTINEL_FILTER}
        """,
    ),
]
