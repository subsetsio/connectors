"""Ofgem Data Portal connector.

Source: the Ofgem (GB energy regulator) Data Portal at
https://www.ofgem.gov.uk/data-portal/all-charts — ~188 interactive charts of
GB energy-market statistics (retail/wholesale prices, debt & arrears, market
shares, customer satisfaction, network performance, renewable-scheme uptake).

Mechanism (per research, chosen = ``everviz_inject``): every chart is rendered
by everviz (Highcharts' hosted SaaS). ``GET https://app.everviz.com/inject/
{token}/`` returns a JS inject script that embeds the full Highcharts options
object inline; the raw numbers live in ``options.data.csv`` — a CSV string
whose item delimiter is either ',' or ';' (both occur, detected per chart),
first column = the x-axis category (date/quarter/label), remaining columns =
named series. The everviz token for each chart comes from the data-portal
listing API and is pinned per chart in ``ENTITY_TOKENS`` below (built at
implement time from the collect catalog).

Fetch shape: stateless full re-pull. Each chart is a tiny table (<50KB) with no
incremental filter (research: "no incremental — full corpus per refresh"), so
every refresh re-fetches and overwrites. Each chart is normalised to a uniform
long format — (category, series, value) — and published as its own Delta table.
"""

import csv as _csv
import io
import json
import re


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

INJECT_URL = "https://app.everviz.com/inject/{token}/"


@transient_retry()
def _fetch_inject(token: str) -> str:
    resp = get(INJECT_URL.format(token=token), timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _balanced_object(s: str, start: int) -> str | None:
    """Return the brace-balanced ``{...}`` substring beginning at ``start``,
    respecting JSON string quoting/escapes."""
    depth = 0
    in_str = False
    esc = False
    for j in range(start, len(s)):
        c = s[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return s[start : j + 1]
    return None


def _extract_options(js: str) -> dict:
    """Extract the inline Highcharts options object from an everviz inject
    script. The script assigns ``options = { ... }``; we slice that object out
    and JSON-parse it."""
    m = re.search(r"options\s*=\s*", js)
    if not m:
        raise ValueError("everviz inject: no `options =` assignment found")
    brace = js.find("{", m.end() - 1)
    if brace < 0:
        raise ValueError("everviz inject: options assignment has no object")
    obj = _balanced_object(js, brace)
    if obj is None:
        raise ValueError("everviz inject: unbalanced options object")
    return json.loads(obj)


def _detect_delimiter(header_line: str) -> str:
    best, best_n = ",", 0
    for d in (",", ";"):
        n = len(next(_csv.reader([header_line], delimiter=d)))
        if n > best_n:
            best, best_n = d, n
    return best


def _parse_value(cell: str):
    cell = (cell or "").strip()
    if cell in ("", "-", "n/a", "N/A", "NA", "null", "None"):
        return None
    try:
        return float(cell)
    except ValueError:
        return None


def _csv_to_long(csv_text: str) -> list[dict]:
    """Normalise a Highcharts ``data.csv`` blob to long format: one row per
    (category, series) cell. Column 0 is the x-axis category; every other
    column is a named numeric series."""
    text = csv_text.replace("\r\n", "\n").replace("\r", "\n")
    first_nl = text.find("\n")
    header_line = text if first_nl < 0 else text[:first_nl]
    delim = _detect_delimiter(header_line)
    reader = list(_csv.reader(io.StringIO(text), delimiter=delim))
    if not reader:
        return []
    header = reader[0]
    series_names = [(h.strip() or f"series_{i}") for i, h in enumerate(header)]
    rows: list[dict] = []
    for rec in reader[1:]:
        if not rec or not any(c.strip() for c in rec):
            continue
        category = (rec[0] or "").strip()
        for i in range(1, len(rec)):
            if i >= len(series_names):
                break
            value = _parse_value(rec[i])
            rows.append(
                {
                    "category": category,
                    "series": series_names[i],
                    "value": value,
                }
            )
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    chart_id = node_id[len("ofgem-") :]
    token = ENTITY_TOKENS[chart_id]
    js = _fetch_inject(token)
    options = _extract_options(js)
    data = options.get("data") or {}
    csv_text = data.get("csv")
    if not csv_text:
        raise ValueError(f"{node_id}: everviz options has no data.csv")
    rows = _csv_to_long(csv_text)
    save_raw_ndjson(rows, asset)


ENTITY_TOKENS = {
    '174996': '8mVG4XDzJ',
    '174997': 'QG6XVhNPt',
    '175002': '0qQ53N8P8',
    '175003': 'TlN419l77',
    '175004': 'AAWy0zrVd',
    '175005': 'SHlCCthnE',
    '175006': 'iJkOJi97A',
    '175007': 'oJdJwK0mD',
    '175008': 'gvS7WsWVw',
    '175009': 'qrr9QdzQD',
    '175010': 'GZOZpyFkv',
    '175011': 'xnd7z6ung',
    '175012': '3msomze67',
    '175013': 'OwOGYf5yf',
    '175014': 'X1W-oTCfR',
    '175015': 'fffNyscXl',
    '175016': 'pCi7dXCNt',
    '175017': 'E-nZ_3blQ',
    '175022': '2cH8g32K2',
    '175023': 'zc4eEpjjH',
    '175024': 'ik8nz8Sl5',
    '175025': 'Uxxu4mVBf',
    '175026': 'UV3CJbvKm',
    '175027': '62T10f3vPK',
    '175028': 'QsMj3ExZD',
    '175029': 'YujoJDkYn',
    '175030': 'WNJz9GGnf',
    '175031': 'nQnW5Fwg0',
    '175032': '0khWdFMoN',
    '175033': 'V0Vu8BwhH',
    '175034': 'GVD_4CaZX',
    '175035': 'rSxrf1q6A',
    '175036': 'vIRIbuAbA',
    '175037': 'cswMOJwof',
    '175038': 'cF-ZhdCEe',
    '175039': 'rlLVO3fAy',
    '175040': 'rOHpNBrvN',
    '175041': 'g6Gow9Uf8',
    '175042': '1PVEsSF5h',
    '175043': 'M3eryTIgn',
    '175044': 'Dm2Cye57E',
    '175045': 'Bj7ppvwa0',
    '175046': 'mRvzBORjM',
    '175047': 'qVunmJEFF',
    '175048': 'fhZjZWpFM',
    '175049': 'NHeq_u8eI',
    '175050': 'QeWkTst5F',
    '175051': 'KfxNUDTE_',
    '175052': 'sWt-9ss37',
    '175053': 'AYd3_MBwl',
    '175054': 'RqVIyifZ-',
    '175055': 'YFsS4g98P',
    '175056': 'n9WSDfgxc',
    '175058': 'Qrefv0-ZN',
    '175059': 'xGcqovNPN',
    '175062': 'RbkixPAU1',
    '175063': '3lBLuuDsP',
    '175064': '-7wWeiqwF',
    '175065': '_o5LqZ5Dk',
    '175066': 'g53GfRDaf',
    '175067': 'xq5ftxo02',
    '175069': 'eGQWqcSLx',
    '175072': '6O2d-NwIv',
    '175073': 'prXgiD5hy',
    '175078': 'ioDAqyvJr',
    '175079': 'OWxkboWD5',
    '175080': 'C_44TBGG7',
    '175081': 'sMLuVas8y',
    '175082': 'kwGUjGQCz',
    '175083': 'kxEqD0HMB',
    '175084': '4E3aHKJcH',
    '175085': 'AdRNzDGq3',
    '175090': 'bcXwvSpv8',
    '175091': '0umQJxm59',
    '175092': 'kvDlEJ7QL',
    '175093': 'oKyblf-5D',
    '175094': 'euIoqswhF',
    '175095': 'XEOWFmq0o',
    '175096': '5yc8nCDTG',
    '175097': '6irDbFt97',
    '175098': '_isQ0xrrh',
    '175099': 'y75zZRgPn',
    '175100': 'fklE1tNvW',
    '175101': 'Be-tkS79v',
    '175102': 'dcK4-sXpb',
    '175103': 'R-EolD-gB',
    '175104': 'KDCUmja5n',
    '175105': '_QPdzgCsn',
    '175106': 'rvBvmqWjQ',
    '175107': 'Xo_cyZ5FE',
    '175108': '63LDJXmr4',
    '175109': '79mp11Iui',
    '175110': '89tH-XFHT',
    '175111': 'YgNmUTePR',
    '175112': 'ld075Jtf4',
    '175113': 'v53yJK_cI',
    '175114': '7uDOI_4vd',
    '175115': 'gWZmesYYy',
    '175116': 'WZpX9GWw9',
    '175117': 'pxicGwhYy',
    '175118': '5x2IOpZOS',
    '175119': '6yBJnBZV3',
    '175120': 'r16QmISPp',
    '175121': 'fYfgXGCOG',
    '175122': 'WfBgUmoBX',
    '175123': 'febKUWLWPE',
    '175124': 'QbOiYZaJK',
    '175125': 'f5LmQKjpe',
    '175126': 'oSkvi5sqD',
    '175127': 'J2rTDLiBg',
    '175128': 'pbPqXYNFx',
    '175137': 'r8TKxLk5V',
    '175138': 'qRvAxIgho',
    '175139': '4GHD8gVq8',
    '175140': 'bYTwfAv6F',
    '175141': 'NKlKhEial',
    '175142': 'lVeuoASKI',
    '175146': 'HwsiUcYVX',
    '175147': 'V14P-9qfH',
    '175148': 'kEI44bOZy',
    '175149': 'k5Xb3BNyg',
    '175157': '4qFp-LBti',
    '175158': 'B3H1yAIhS',
    '175159': 'KcdezkehJ',
    '175168': 'vHRHzA021',
    '175171': '0eDBSsofl',
    '175172': 'xQHwOz4nR',
    '176093': 'FIUVSADKN',
    '176094': '0IwJatYrR',
    '176095': 'ftCyZiKt2',
    '176999': 'c_y_Dm7Rx',
    '177000': 'fpptIG0Jf',
    '177001': '6EgYhkmDg',
    '177185': 'wGVOqaWps',
    '177187': 'YdfcnXHwg',
    '177277': 'bePMY9qV_',
    '177278': 'gztnd0SgB',
    '179052': '5M_IvDXBd',
    '179227': 'y-0sCALvp',
    '179229': 'KVj-D5pKi',
    '179530': '967faU9lS',
    '180095': 'qhZyBUVII',
}
ENTITY_IDS = list(ENTITY_TOKENS)

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ofgem-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(category AS VARCHAR) AS category,
                CAST(series   AS VARCHAR) AS series,
                CAST(value    AS DOUBLE)  AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
        # Uniform long format: one row per (x-axis category, series) cell.
        key=("category", "series"),
    )
    for s in DOWNLOAD_SPECS
]
