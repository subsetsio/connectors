"""Croatian National Bank (HNB) — daily exchange-rate reference lists.

Source: the HNB exchange-rate-list REST API at https://api.hnb.hr (no auth, JSON).
Two endpoint families cover the same daily FX reference series across the
2023 kuna->euro switch:

  * tecajn-eur/v3 — euro-based (foreign currency per 1 EUR), 2023-01-01 -> present.
  * tecajn/v2     — kuna-based legacy (foreign currency per `jedinica` HRK),
                    1994-05-30 -> 2022-12-31.

Fetch shape: stateless full re-pull (shape 1). The whole corpus is small
(<20MB) and a single wide date-range request per endpoint returns every day in
one response, so we re-pull in full each run and overwrite — revisions are
picked up for free. There is no incremental query parameter on this API.

API quirk (euro endpoint): combining the `valuta` filter with a date range
silently returns only the latest single day, so we range-query WITHOUT a
currency filter and keep all currencies.

Raw is stored verbatim as parquet (all string fields, plus integer `jedinica`
on the kuna table); the numeric rates use a comma decimal separator and are
normalised to DOUBLE in the transform SQL.
"""

from datetime import date

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://api.hnb.hr"

# Euro era opened at adoption; kuna series is frozen at end-2022.
EUR_START = "2023-01-01"
HRK_START = "1994-05-30"
HRK_END = "2022-12-31"

# Verbatim raw schemas (rates kept as strings — comma decimals normalised in SQL).
EUR_SCHEMA = pa.schema([
    ("broj_tecajnice", pa.string()),
    ("datum_primjene", pa.string()),
    ("drzava", pa.string()),
    ("drzava_iso", pa.string()),
    ("valuta", pa.string()),
    ("sifra_valute", pa.string()),
    ("kupovni_tecaj", pa.string()),
    ("prodajni_tecaj", pa.string()),
    ("srednji_tecaj", pa.string()),
])

HRK_SCHEMA = pa.schema([
    ("broj_tecajnice", pa.string()),
    ("datum", pa.string()),
    ("drzava", pa.string()),
    ("jedinica", pa.int64()),
    ("valuta", pa.string()),
    ("sifra_valute", pa.string()),
    ("kupovni_tecaj", pa.string()),
    ("prodajni_tecaj", pa.string()),
    ("srednji_tecaj", pa.string()),
])


@transient_retry()
def _fetch_range(path: str, start: str, end: str) -> list:
    url = f"{BASE}/{path}"
    params = {"datum-primjene-od": start, "datum-primjene-do": end}
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _coerce(rows: list, schema: pa.Schema) -> pa.Table:
    cols = {f.name: f for f in schema}
    out = {name: [] for name in cols}
    for rec in rows:
        for name, field in cols.items():
            val = rec.get(name)
            if field.type == pa.int64():
                out[name].append(int(val) if val is not None else None)
            else:
                out[name].append(str(val) if val is not None else None)
    return pa.table(out, schema=schema)


def fetch_eur(node_id: str) -> None:
    asset = node_id
    today = date.today().isoformat()
    rows = _fetch_range("tecajn-eur/v3", EUR_START, today)
    if not rows:
        raise AssertionError(f"{asset}: euro endpoint returned no rows")
    save_raw_parquet(_coerce(rows, EUR_SCHEMA), asset)


def fetch_hrk(node_id: str) -> None:
    asset = node_id
    rows = _fetch_range("tecajn/v2", HRK_START, HRK_END)
    if not rows:
        raise AssertionError(f"{asset}: kuna endpoint returned no rows")
    save_raw_parquet(_coerce(rows, HRK_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="croatian-national-bank-exchange-rates-eur", fn=fetch_eur, kind="download"),
    NodeSpec(id="croatian-national-bank-exchange-rates-hrk", fn=fetch_hrk, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="croatian-national-bank-exchange-rates-eur-transform",
        deps=["croatian-national-bank-exchange-rates-eur"],
        sql='''
            SELECT DISTINCT
                CAST(datum_primjene AS DATE)                      AS date,
                valuta                                            AS currency,
                drzava                                            AS country,
                drzava_iso                                        AS country_iso,
                sifra_valute                                      AS currency_numeric,
                CAST(REPLACE(kupovni_tecaj,  ',', '.') AS DOUBLE) AS buying_rate,
                CAST(REPLACE(srednji_tecaj,  ',', '.') AS DOUBLE) AS middle_rate,
                CAST(REPLACE(prodajni_tecaj, ',', '.') AS DOUBLE) AS selling_rate,
                CAST(broj_tecajnice AS INTEGER)                   AS bulletin_number
            FROM "croatian-national-bank-exchange-rates-eur"
            WHERE valuta IS NOT NULL AND datum_primjene IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="croatian-national-bank-exchange-rates-hrk-transform",
        deps=["croatian-national-bank-exchange-rates-hrk"],
        sql='''
            SELECT DISTINCT
                CAST(datum AS DATE)                               AS date,
                valuta                                            AS currency,
                drzava                                            AS country,
                jedinica                                          AS unit,
                sifra_valute                                      AS currency_numeric,
                CAST(REPLACE(kupovni_tecaj,  ',', '.') AS DOUBLE) AS buying_rate,
                CAST(REPLACE(srednji_tecaj,  ',', '.') AS DOUBLE) AS middle_rate,
                CAST(REPLACE(prodajni_tecaj, ',', '.') AS DOUBLE) AS selling_rate,
                CAST(broj_tecajnice AS INTEGER)                   AS bulletin_number
            FROM "croatian-national-bank-exchange-rates-hrk"
            WHERE valuta IS NOT NULL AND datum IS NOT NULL
        ''',
    ),
]
