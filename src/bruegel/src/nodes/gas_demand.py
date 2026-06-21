"""European Natural Gas Demand Tracker — JS dashboard backed by the GitHub repo
benmcwilliams/gas-demand; cleaned monthly demand JSON is fetched directly."""
from subsets_utils import NodeSpec, SqlNodeSpec
from utils import clean, get_bytes, run_download

EID = "european-natural-gas-demand-tracker"
DEP = f"bruegel-{EID}"


def parse(_links):
    """JS dashboard backed by GitHub repo benmcwilliams/gas-demand. The cleaned
    monthly data (by country and sector) lives as tidy JSON on the default branch.
    y_value is TWh deviation vs the 2019-2021 monthly-average baseline."""
    import json
    url = ("https://raw.githubusercontent.com/benmcwilliams/gas-demand/"
           "main/highcharts/data/monthly_demand_sector.json")
    raw = json.loads(get_bytes(url))
    out = []
    for r in raw:
        x = str(r.get("x_value", ""))
        if "/" not in x:
            continue
        mm, yyyy = x.split("/")
        val = r.get("y_value")
        if val is None:
            continue
        out.append({"date": f"{yyyy}-{int(mm):02d}-01",
                    "country": r.get("group_b_value"),
                    "sector": r.get("group_value"),
                    "value": clean(val)})
    return out


def fetch(node_id: str) -> None:
    run_download(node_id, None, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT CAST(date AS DATE) AS date, country, sector,
               CAST(value AS DOUBLE) AS demand_twh_dev
        FROM "{dep}" WHERE value IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
