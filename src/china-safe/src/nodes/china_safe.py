"""SAFE (State Administration of Foreign Exchange, China) — china-safe.

Mechanism: the public structured-data query app ('结构化数据综合管理', behind the
统计数据跨表查询 / cross-table query page) at
https://www.safe.gov.cn/AppStructured/hlw/. Exactly 11 publishable statistical
tables (rank-active subset of the 12 codes the app exposes), each a complete time
series. Three endpoints per table:

  - getProjectOption.do?tableCode=<code>  (GET)  -> the table's project row-items
    as <option> HTML.
  - queryDate.do  (POST param=<projects joined by '=='>, codes=<comma codes>)
    -> JSON array of available period codes (annual 'YYYY' and/or monthly 'YYYYMM').
  - advQuery2.do  (POST codeList/projectNames/projectBean.projectNames/years/queryYN)
    -> a full HTML page whose <table id="InfoTable"> carries the data: header row
    [表名称, 项目名称(单位), period...], then one data row per project
    [table_name, project, value...] (values comma-formatted; blank = no datum).

Fetch shape: stateless full re-pull. One advQuery2 POST returns every project x
every period for a table, so the whole corpus is a handful of small requests —
re-fetched and overwritten each run, which picks up revisions for free.

Anti-automation: advQuery2.do (and the metadata endpoints under burst load) return
HTTP 500 with a site '该页面不存在' page when the per-IP request rate is tripped.
This is transient — the canonical tenacity retry with exponential backoff treats
5xx and the block-page body as retryable, which paces us back under the limit.
All labels and values are Chinese; values are numeric (units are embedded in the
project label, e.g. '(单位：亿美元)').
"""

import re
import html
import time

import httpx
import pyarrow as pa
from urllib.parse import urlencode
from tenacity import (
    retry, retry_if_exception, stop_after_attempt, wait_exponential, wait_random,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, post, save_raw_parquet

# Entity union — rank-active table codes (the 12th, G2, scored below threshold).
ENTITY_IDS = ["A21", "A22", "B21", "C2", "H2", "I2", "J2", "YY12", "YY13", "YY21", "YY22"]

_BASE = "https://www.safe.gov.cn/AppStructured/hlw/"
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Referer": _BASE + "advQuery.do",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
_FORM_HEADERS = dict(_HEADERS, **{"Content-Type": "application/x-www-form-urlencoded"})

_RAW_SCHEMA = pa.schema([
    ("table_code", pa.string()),
    ("table_name", pa.string()),
    ("project", pa.string()),
    ("period", pa.string()),
    ("value", pa.float64()),
])

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


class _Blocked(Exception):
    """SAFE's anti-automation block page / 5xx — retryable, eventually clears."""


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, (_Blocked, _TRANSIENT_EXC)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


def _check_block(text: str, status: int, where: str) -> None:
    if status >= 500 or "该页面不存在" in text:
        raise _Blocked(f"{where}: anti-automation block (status={status})")


@retry(retry=retry_if_exception(_is_transient), stop=stop_after_attempt(8),
       wait=wait_exponential(min=5, max=120) + wait_random(0, 4), reraise=True)
def _get_projects(code: str) -> list:
    r = get(_BASE + "getProjectOption.do", params={"tableCode": code},
            headers=_HEADERS, timeout=(10.0, 60.0))
    _check_block(r.text, r.status_code, "getProjectOption")
    r.raise_for_status()
    projects = [html.unescape(o) for o in re.findall(r"<option value='([^']*)'>", r.text) if o]
    # An empty 200 here is the anti-automation rate-limit (these 11 tables always
    # have projects) — raise so the retry backoff paces us back under the limit.
    if not projects:
        raise _Blocked(f"getProjectOption {code}: empty project list (rate-limited)")
    return projects


@retry(retry=retry_if_exception(_is_transient), stop=stop_after_attempt(8),
       wait=wait_exponential(min=5, max=120) + wait_random(0, 4), reraise=True)
def _get_periods(code: str, projects: list) -> list:
    body = urlencode({
        "param": "".join(p + "==" for p in projects),
        "codes": ",".join(code for _ in projects) + ",",
    })
    r = post(_BASE + "queryDate.do", content=body.encode("utf-8"),
             headers=_FORM_HEADERS, timeout=(10.0, 60.0))
    _check_block(r.text, r.status_code, "queryDate")
    r.raise_for_status()
    periods = re.findall(r'"(\d+)"', r.text)
    # Empty 200 = rate-limit (every table has periods) — retry under backoff.
    if not periods:
        raise _Blocked(f"queryDate {code}: empty period list (rate-limited)")
    return periods


@retry(retry=retry_if_exception(_is_transient), stop=stop_after_attempt(8),
       wait=wait_exponential(min=5, max=120) + wait_random(0, 4), reraise=True)
def _query_table(code: str, projects: list, periods: list) -> str:
    pairs = (
        [("codeList", code) for _ in projects]
        + [("projectNames", p) for p in projects]
        + [("projectBean.projectNames", p) for p in projects]
        + [("years", y) for y in periods]
        + [("queryYN", "true")]
    )
    r = post(_BASE + "advQuery2.do", content=urlencode(pairs).encode("utf-8"),
             headers=_FORM_HEADERS, timeout=(15.0, 180.0))
    _check_block(r.text, r.status_code, "advQuery2")
    r.raise_for_status()
    return r.text


def _cell_text(cell_html: str) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(cell_html)).strip()


def _clean_project(text: str) -> str:
    # The project cell carries a stray HTML-comment terminator before the label.
    return text.split("-->")[-1].strip()


def _parse_value(text: str):
    t = text.replace(",", "").strip()
    if not t or t in {"-", "--", "...", "—"}:
        return None
    try:
        return float(t)
    except ValueError:
        return None


def _parse_info_table(page_html: str):
    """Yield (table_name, project, period, value) from <table id='InfoTable'>."""
    m = re.search(r'<table[^>]*id="InfoTable".*?</table>', page_html, re.S)
    if not m:
        raise AssertionError("InfoTable not found in advQuery2 response")
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(0), re.S)
    if len(rows) < 2:
        raise AssertionError(f"InfoTable has {len(rows)} rows; expected >= 2")
    header = [_cell_text(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", rows[0], re.S)]
    periods = header[2:]  # cols 0,1 = 表名称, 项目名称(单位)
    for row in rows[1:]:
        cells = [_cell_text(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S)]
        if len(cells) < 2:
            continue
        table_name = cells[0].strip()
        project = _clean_project(cells[1])
        for period, raw in zip(periods, cells[2:]):
            value = _parse_value(raw)
            if value is not None:
                yield table_name, project, period, value


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    code = node_id.removeprefix("china-safe-").upper()  # codes are uppercase, no '_'

    projects = _get_projects(code)
    assert projects, f"{code}: getProjectOption returned no projects"
    time.sleep(2)
    periods = _get_periods(code, projects)
    assert periods, f"{code}: queryDate returned no periods"
    time.sleep(2)
    page = _query_table(code, projects, periods)

    rows = list(_parse_info_table(page))
    assert rows, f"{code}: parsed 0 (project, period, value) rows from advQuery2"

    table = pa.table({
        "table_code": [code] * len(rows),
        "table_name": [r[0] for r in rows],
        "project": [r[1] for r in rows],
        "period": [r[2] for r in rows],
        "value": [r[3] for r in rows],
    }, schema=_RAW_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"china-safe-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per table. Normalize the mixed annual/monthly period
# code into a frequency flag + a real date (annual -> Jan 1, monthly -> month 1),
# keeping the raw period string so annual/monthly rows of the same year stay
# distinct. Comma-stripping happened in the fetch; here we just type and reshape.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                table_code,
                table_name,
                project,
                period,
                CASE
                    WHEN length(period) = 4 THEN 'annual'
                    WHEN length(period) = 6 THEN 'monthly'
                    ELSE 'other'
                END AS frequency,
                CASE
                    WHEN length(period) = 4
                        THEN make_date(CAST(period AS INTEGER), 1, 1)
                    WHEN length(period) = 6
                        THEN make_date(CAST(substr(period, 1, 4) AS INTEGER),
                                       CAST(substr(period, 5, 2) AS INTEGER), 1)
                    ELSE NULL
                END AS date,
                CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
