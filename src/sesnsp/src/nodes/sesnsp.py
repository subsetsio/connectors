"""SESNSP Incidencia Delictiva raw downloads.

The source exposes one CKAN package with three CSV resources. The state file is
already long-format; the municipal and victim files are wide by month, so the
download normalizes them to one row per month and writes typed parquet. This
keeps raw SQL-readable and gives every asset a comparable `fecha` freshness
column for the monthly release cadence.
"""

from __future__ import annotations

import io

import httpx
import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet


PACKAGE_URL = "https://www.datos.gob.mx/api/3/action/package_show?id=incidencia_delictiva"
PREFIX = "sesnsp-"

STATE_ID = "d9b2792a-33a2-4ea8-8527-210d9e99de5e"
MUNICIPAL_ID = "57fbd692-3e5c-4b1b-8621-694cb3a33035"
VICTIMS_ID = "386f17d2-a488-4da2-9c85-99765b5a9cdc"

FALLBACK_URLS = {
    STATE_ID: "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_dic25.csv",
    MUNICIPAL_ID: "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/IDM_NM_dic25.csv",
    VICTIMS_ID: "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/IDVFC_NM_dic25.csv",
}

MONTHS = {
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12,
}


STATE_SCHEMA = pa.schema(
    [
        ("anio", pa.int64()),
        ("clave_ent", pa.string()),
        ("entidad", pa.string()),
        ("bien_juridico_afectado", pa.string()),
        ("tipo_delito", pa.string()),
        ("subtipo_delito", pa.string()),
        ("modalidad", pa.string()),
        ("mes", pa.string()),
        ("fecha", pa.date32()),
        ("incidencia_delictiva", pa.int64()),
        ("entidad_federativa", pa.string()),
    ]
)

MUNICIPAL_SCHEMA = pa.schema(
    [
        ("anio", pa.int64()),
        ("clave_ent", pa.string()),
        ("entidad", pa.string()),
        ("cve_municipio", pa.string()),
        ("municipio", pa.string()),
        ("bien_juridico_afectado", pa.string()),
        ("tipo_delito", pa.string()),
        ("subtipo_delito", pa.string()),
        ("modalidad", pa.string()),
        ("mes", pa.string()),
        ("fecha", pa.date32()),
        ("incidencia_delictiva", pa.int64()),
    ]
)

VICTIMS_SCHEMA = pa.schema(
    [
        ("anio", pa.int64()),
        ("clave_ent", pa.string()),
        ("entidad", pa.string()),
        ("bien_juridico_afectado", pa.string()),
        ("tipo_delito", pa.string()),
        ("subtipo_delito", pa.string()),
        ("modalidad", pa.string()),
        ("sexo", pa.string()),
        ("rango_edad", pa.string()),
        ("mes", pa.string()),
        ("fecha", pa.date32()),
        ("victimas", pa.int64()),
    ]
)


def _client() -> httpx.Client:
    return httpx.Client(
        follow_redirects=True,
        headers={"User-Agent": "subsets.io sesnsp connector"},
        timeout=httpx.Timeout(300.0, connect=30.0),
        verify=False,
    )


def _resource_id(node_id: str) -> str:
    if not node_id.startswith(PREFIX):
        raise ValueError(f"unexpected SESNSP node id: {node_id}")
    return node_id.removeprefix(PREFIX)


def _current_resource_urls() -> dict[str, str]:
    try:
        with _client() as client:
            response = client.get(PACKAGE_URL)
            response.raise_for_status()
            package = response.json()["result"]
    except Exception:
        return dict(FALLBACK_URLS)

    urls = {}
    for resource in package.get("resources", []):
        if resource.get("state") != "active":
            continue
        if resource.get("format", "").upper() != "CSV":
            continue
        url = resource.get("url") or resource.get("original_url")
        if url:
            urls[resource["id"]] = url
    return {**FALLBACK_URLS, **urls}


def _download(url: str) -> bytes:
    with _client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.content


def _coerce_int(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def _month_date_frame(years: pd.Series, months: pd.Series) -> pd.Series:
    month_nums = months.map(MONTHS).astype("Int64")
    dates = {
        "year": _coerce_int(years),
        "month": month_nums,
        "day": 1,
    }
    return pd.to_datetime(pd.DataFrame(dates), errors="coerce").dt.date


def _table(df: pd.DataFrame, schema: pa.Schema) -> pa.Table:
    for field in schema:
        if pa.types.is_integer(field.type):
            df[field.name] = _coerce_int(df[field.name])
        elif pa.types.is_string(field.type):
            df[field.name] = df[field.name].astype("string")
    return pa.Table.from_pandas(df[list(schema.names)], schema=schema, preserve_index=False)


def _read_csv(content: bytes, *, encoding: str, dtype: dict[str, str] | None = None) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(content), encoding=encoding, dtype=dtype or {}, low_memory=False)


def _fetch_state(url: str) -> pa.Table:
    df = _read_csv(url and _download(url), encoding="utf-8", dtype={"clave_ent": "string"})
    df = df.rename(columns={"incidencia_delictiva": "incidencia_delictiva"})
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date
    return _table(df, STATE_SCHEMA)


def _melt_months(df: pd.DataFrame, *, value_name: str) -> pd.DataFrame:
    out = df.melt(
        id_vars=[col for col in df.columns if col not in MONTHS],
        value_vars=list(MONTHS),
        var_name="mes",
        value_name=value_name,
    )
    out["fecha"] = _month_date_frame(out["anio"], out["mes"])
    return out


def _fetch_municipal(url: str) -> pa.Table:
    df = _read_csv(
        _download(url),
        encoding="latin1",
        dtype={"Clave_Ent": "string", "Cve. Municipio": "string"},
    )
    df = df.rename(
        columns={
            "Año": "anio",
            "Clave_Ent": "clave_ent",
            "Entidad": "entidad",
            "Cve. Municipio": "cve_municipio",
            "Municipio": "municipio",
            "Bien jurídico afectado": "bien_juridico_afectado",
            "Tipo de delito": "tipo_delito",
            "Subtipo de delito": "subtipo_delito",
            "Modalidad": "modalidad",
        }
    )
    df = _melt_months(df, value_name="incidencia_delictiva")
    return _table(df, MUNICIPAL_SCHEMA)


def _fetch_victims(url: str) -> pa.Table:
    df = _read_csv(_download(url), encoding="latin1", dtype={"Clave_Ent": "string"})
    df = df.rename(
        columns={
            "Año": "anio",
            "Clave_Ent": "clave_ent",
            "Entidad": "entidad",
            "Bien jurídico afectado": "bien_juridico_afectado",
            "Tipo de delito": "tipo_delito",
            "Subtipo de delito": "subtipo_delito",
            "Modalidad": "modalidad",
            "Sexo": "sexo",
            "Rango de edad": "rango_edad",
        }
    )
    df = _melt_months(df, value_name="victimas")
    return _table(df, VICTIMS_SCHEMA)


def fetch_one(node_id: str) -> None:
    resource_id = _resource_id(node_id)
    url = _current_resource_urls()[resource_id]
    if resource_id == STATE_ID:
        table = _fetch_state(url)
    elif resource_id == MUNICIPAL_ID:
        table = _fetch_municipal(url)
    elif resource_id == VICTIMS_ID:
        table = _fetch_victims(url)
    else:
        raise ValueError(f"unhandled SESNSP resource id: {resource_id}")
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{VICTIMS_ID}", fn=fetch_one, kind="download"),
    NodeSpec(id=f"{PREFIX}{MUNICIPAL_ID}", fn=fetch_one, kind="download"),
    NodeSpec(id=f"{PREFIX}{STATE_ID}", fn=fetch_one, kind="download"),
]
