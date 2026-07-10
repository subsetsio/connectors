"""sec-companies — EDGAR filer reference table (cik, name, ticker, exchange),
from www.sec.gov/files/company_tickers_exchange.json."""
import pyarrow as pa

from subsets_utils import configure_http, save_raw_parquet
from utils import USER_AGENT, fetch_json

COMPANIES_SCHEMA = pa.schema([
    ("cik", pa.int64()),
    ("name", pa.string()),
    ("ticker", pa.string()),
    ("exchange", pa.string()),
])


def fetch_companies(node_id: str) -> None:
    asset = node_id
    configure_http(headers={"User-Agent": USER_AGENT})
    data = fetch_json("https://www.sec.gov/files/company_tickers_exchange.json")
    idx = {field: i for i, field in enumerate(data["fields"])}
    rows = [
        {
            "cik": rec[idx["cik"]],
            "name": rec[idx["name"]],
            "ticker": rec[idx["ticker"]],
            "exchange": rec[idx["exchange"]],
        }
        for rec in data["data"]
    ]
    table = pa.Table.from_pylist(rows, schema=COMPANIES_SCHEMA)
    save_raw_parquet(table, asset)
