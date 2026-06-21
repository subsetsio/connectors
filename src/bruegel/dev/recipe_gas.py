"""Dataset 1: european-natural-gas-demand-tracker — TESTED recipe."""
import json, httpx

URL = "https://raw.githubusercontent.com/benmcwilliams/gas-demand/main/highcharts/data/monthly_demand_sector.json"

def load_gas_demand():
    raw = httpx.get(URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"}).json()
    rows = []
    for r in raw:
        mm, yyyy = r["x_value"].split("/")           # 'MM/YYYY'
        rows.append({
            "date": f"{yyyy}-{mm}-01",                # first of month
            "country": r["group_b_value"],
            "sector": r["group_value"],               # power|industry|household|industry-household|total
            "value": r["y_value"],                    # TWh deviation vs 2019-2021 monthly-avg baseline
        })
    return rows

if __name__ == "__main__":
    rows = load_gas_demand()
    print("TOTAL ROWS:", len(rows))
    for r in rows[:5]:
        print(r)
