"""SIAP open-data downloads.

DGSIAP publishes annual agricultural and livestock production CSV attachments
from catalog pages. Each accepted subset is one domain/level schema across all
listed years, so each download node fetches every year for that schema and
stores one normalized parquet raw asset.
"""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet


BASE_URL = "https://nube.agricultura.gob.mx/index.php"


AGRICOLA_MUNICIPAL_YEARS = tuple(range(2003, 2025))
AGRICOLA_NACIONAL_YEARS = tuple(range(1980, 2003))
PECUARIO_MUNICIPAL_YEARS = tuple(list(range(2006, 2023)) + [2024])
PECUARIO_NACIONAL_YEARS = tuple(range(1980, 2006))


AGRICOLA_MUNICIPAL_VIEW = "10AE434F-A2158368-A120BC5A-EDF4AFAA"
AGRICOLA_NACIONAL_VIEW = "5F687BE6-1513BEE9-53E63085-9D3C988B"
PECUARIO_MUNICIPAL_VIEW = "E370DEBE-390827E8-72838350-94616860"
PECUARIO_NACIONAL_VIEW = "31AF5807-EB5F517E-74C6BB9A-E4EBD17F"


AGRICOLA_MUNICIPAL_COLUMNS = (
    "source_year",
    "anio",
    "idestado",
    "nomestado",
    "idddr",
    "nomddr",
    "idcader",
    "nomcader",
    "idmunicipio",
    "nommunicipio",
    "idciclo",
    "nomcicloproductivo",
    "idmodalidad",
    "nommodalidad",
    "idunidadmedida",
    "nomunidad",
    "idcultivo",
    "nomcultivo",
    "sembrada",
    "cosechada",
    "siniestrada",
    "volumenproduccion",
    "rendimiento",
    "precio",
    "valorproduccion",
)

AGRICOLA_NACIONAL_COLUMNS = (
    "source_year",
    "anio",
    "idestado",
    "nomestado",
    "idciclo",
    "nomcicloproductivo",
    "idmodalidad",
    "nommodalidad",
    "idunidadmedida",
    "nomunidad",
    "idcultivo",
    "nomcultivo",
    "sembrada",
    "cosechada",
    "siniestrada",
    "volumenproduccion",
    "rendimiento",
    "precio",
    "valorproduccion",
)

PECUARIO_MUNICIPAL_COLUMNS = (
    "source_year",
    "anio",
    "cveestado",
    "nomestado",
    "cveddr",
    "nomddr",
    "cvempio",
    "nommunicipio",
    "cveespecie",
    "nomespecie",
    "cveproducto",
    "nomproducto",
    "volumen",
    "peso",
    "precio",
    "valor",
    "asacrificado",
)

PECUARIO_NACIONAL_COLUMNS = (
    "source_year",
    "anio",
    "cveestado",
    "nomestado",
    "cveespecie",
    "nomespecie",
    "cveproducto",
    "nomproducto",
    "volumen",
    "peso",
    "precio",
    "valor",
    "asacrificado",
)


NUMERIC_COLUMNS = {
    "sembrada",
    "cosechada",
    "siniestrada",
    "volumenproduccion",
    "rendimiento",
    "precio",
    "valorproduccion",
    "volumen",
    "peso",
    "valor",
    "asacrificado",
}


RENAMES = {
    "Anio": "anio",
    "Idestado": "idestado",
    "Nomestado": "nomestado",
    "Idddr": "idddr",
    "Nomddr": "nomddr",
    "Idcader": "idcader",
    "Nomcader": "nomcader",
    "Idmunicipio": "idmunicipio",
    "Nommunicipio": "nommunicipio",
    "Idciclo": "idciclo",
    "Nomcicloproductivo": "nomcicloproductivo",
    "Idmodalidad": "idmodalidad",
    "Nommodalidad": "nommodalidad",
    "Idunidadmedida": "idunidadmedida",
    "Nomunidad": "nomunidad",
    "Idcultivo": "idcultivo",
    "Nomcultivo": "nomcultivo",
    "Nomcultivo Sin Um": "nomcultivo",
    "Sembrada": "sembrada",
    "Cosechada": "cosechada",
    "Siniestrada": "siniestrada",
    "Volumenproduccion": "volumenproduccion",
    "Rendimiento": "rendimiento",
    "Precio": "precio",
    "Preciomediorural": "precio",
    "Valorproduccion": "valorproduccion",
    "Cveestado": "cveestado",
    "Cveddr": "cveddr",
    "Cvempio": "cvempio",
    "Cveespecie": "cveespecie",
    "Nomespecie": "nomespecie",
    "Cveproducto": "cveproducto",
    "Nomproducto": "nomproducto",
    "Volumen": "volumen",
    "Peso": "peso",
    "Valor": "valor",
    "Asacrificado": "asacrificado",
}


def _schema(columns: tuple[str, ...]) -> pa.Schema:
    fields = []
    for name in columns:
        if name in {"source_year", "anio"}:
            typ = pa.int64()
        elif name in NUMERIC_COLUMNS:
            typ = pa.float64()
        else:
            typ = pa.string()
        fields.append(pa.field(name, typ))
    return pa.schema(fields)


def _download_csv(view_id: str, year: int) -> bytes:
    resp = get(
        BASE_URL,
        params={"view": view_id, "ANIO": year},
        timeout=(10.0, 240.0),
        headers={"Accept": "text/csv,*/*"},
    )
    resp.raise_for_status()
    content = resp.content
    if not content.startswith(b"Anio,"):
        raise AssertionError(f"{view_id} {year}: response did not start with CSV header")
    return content


def _read_year(view_id: str, year: int, columns: tuple[str, ...]) -> pd.DataFrame:
    content = _download_csv(view_id, year)
    df = pd.read_csv(
        BytesIO(content),
        encoding="latin1",
        dtype=str,
        keep_default_na=False,
    )
    df = df.loc[:, [c for c in df.columns if str(c).strip()]]
    df = df.rename(columns={c: RENAMES.get(str(c).strip(), str(c).strip()) for c in df.columns})
    df["source_year"] = year

    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise AssertionError(f"{view_id} {year}: missing expected columns {missing}")
    df = df.loc[:, list(columns)].copy()

    for col in columns:
        if col in {"source_year", "anio"}:
            df[col] = pd.to_numeric(df[col], errors="raise").astype("int64")
        elif col in NUMERIC_COLUMNS:
            df[col] = pd.to_numeric(df[col].replace("", pd.NA), errors="coerce")
        else:
            df[col] = df[col].replace("", pd.NA)
    if df.empty:
        raise AssertionError(f"{view_id} {year}: CSV had no data rows")
    return df


def _fetch_years(
    node_id: str,
    *,
    view_id: str,
    years: tuple[int, ...],
    columns: tuple[str, ...],
) -> None:
    frames = [_read_year(view_id, year, columns) for year in years]
    df = pd.concat(frames, ignore_index=True)
    table = pa.Table.from_pandas(df, schema=_schema(columns), preserve_index=False)
    if table.num_rows == 0:
        raise AssertionError(f"{node_id}: no rows after combining {len(years)} years")
    save_raw_parquet(table, node_id)


def fetch_agricola_municipal(node_id: str) -> None:
    _fetch_years(
        node_id,
        view_id=AGRICOLA_MUNICIPAL_VIEW,
        years=AGRICOLA_MUNICIPAL_YEARS,
        columns=AGRICOLA_MUNICIPAL_COLUMNS,
    )


def fetch_agricola_nacional(node_id: str) -> None:
    _fetch_years(
        node_id,
        view_id=AGRICOLA_NACIONAL_VIEW,
        years=AGRICOLA_NACIONAL_YEARS,
        columns=AGRICOLA_NACIONAL_COLUMNS,
    )


def fetch_pecuario_municipal(node_id: str) -> None:
    _fetch_years(
        node_id,
        view_id=PECUARIO_MUNICIPAL_VIEW,
        years=PECUARIO_MUNICIPAL_YEARS,
        columns=PECUARIO_MUNICIPAL_COLUMNS,
    )


def fetch_pecuario_nacional(node_id: str) -> None:
    _fetch_years(
        node_id,
        view_id=PECUARIO_NACIONAL_VIEW,
        years=PECUARIO_NACIONAL_YEARS,
        columns=PECUARIO_NACIONAL_COLUMNS,
    )


DOWNLOAD_SPECS = [
    NodeSpec(id="siap-agricola-municipal", fn=fetch_agricola_municipal, kind="download"),
    NodeSpec(id="siap-agricola-nacional", fn=fetch_agricola_nacional, kind="download"),
    NodeSpec(id="siap-pecuario-municipal", fn=fetch_pecuario_municipal, kind="download"),
    NodeSpec(id="siap-pecuario-nacional", fn=fetch_pecuario_nacional, kind="download"),
]
