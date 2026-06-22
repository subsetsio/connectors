"""EU Labour Market Outlook Dashboard — ZIP wrapping a .7z that contains the
"timeseries- all" Excel workbook; emitted as long (year, country, indicator)."""
import io
import zipfile

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import get_bytes, run_download

EID = "eu-labour-market-outlook-dashboard"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/eu-labour-market-outlook-dashboard"


def parse(links):
    import os
    import tempfile

    import py7zr
    import openpyxl

    zip_url = [u for u in links if u.lower().endswith(".zip")][0]
    zbytes = get_bytes(zip_url)
    with zipfile.ZipFile(io.BytesIO(zbytes)) as zf:
        inner = next(n for n in zf.namelist() if n.lower().endswith(".7z"))
        seven = zf.read(inner)
    out = []
    with tempfile.TemporaryDirectory() as td:
        with py7zr.SevenZipFile(io.BytesIO(seven), "r") as z:
            target = next(n for n in z.getnames()
                          if n.lower().endswith(".xlsx") and "timeseries- all" in n.lower())
            z.extract(path=td, targets=[target])
        wb = openpyxl.load_workbook(os.path.join(td, target), read_only=True, data_only=True)
        ws = wb["Sheet1"]
        it = ws.iter_rows(values_only=True)
        next(it)  # header: Year, Country, Breakdown(indicator), Variable, Value, Variable2(label)...
        for r in it:
            year, country, indicator, _code, value, group_label = r[0], r[1], r[2], r[3], r[4], r[5]
            if year is None or value is None:
                continue
            out.append({"year": int(year), "country": country,
                        "indicator": indicator, "breakdown": group_label,
                        "value": float(value)})
    return out


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT CAST(year AS INTEGER) AS year, country, indicator, breakdown,
               CAST(value AS DOUBLE) AS value
        FROM "{dep}" WHERE value IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
