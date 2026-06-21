"""European Clean Tech Tracker — Next.js app (no downloadable file/API). Only
/investments/overview exposes machine-readable chart data in its RSC payload;
we extract the Highcharts {categories, series} object and flatten to long."""
import re

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import clean, get_text, run_download

EID = "european-clean-tech-tracker"
DEP = f"bruegel-{EID}"

_CLEANTECH_BASE = "https://european-clean-tech-tracker.bruegel.org"


def _match_brace(s, start):
    depth, i, instr, esc = 0, start, False, False
    while i < len(s):
        c = s[i]
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == '"':
            instr = not instr
        elif not instr:
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def parse(_links):
    import json
    rsc = get_text(_CLEANTECH_BASE + "/investments/overview", headers={"RSC": "1"})
    out = []
    for m in re.finditer(r'\{"categories"', rsc):
        end = _match_brace(rsc, m.start())
        if end < 0:
            continue
        block = rsc[m.start():end + 1].replace('"$undefined"', "null")
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue
        if "categories" not in obj or "series" not in obj:
            continue
        cats = obj["categories"]
        for s in obj["series"]:
            for cat, val in zip(cats, s.get("data") or []):
                if val is None:
                    continue
                out.append({"category": clean(cat), "series": s.get("name"),
                            "value": clean(val)})
    return out


def fetch(node_id: str) -> None:
    run_download(node_id, None, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT category AS destination_country, series AS project_status,
               TRY_CAST(value AS DOUBLE) AS investment_eur
        FROM "{dep}" WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
