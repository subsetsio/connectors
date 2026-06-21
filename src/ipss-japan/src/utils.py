"""Shared HTTP + parse helpers for the IPSS (Japan) Japanese Mortality
Database (JMD) connector.

The JMD is an IPSS clone of the Human Mortality Database covering 48 areas
(All Japan = code 00, plus the 47 prefectures 01-47). Every series is a static
whitespace-delimited .txt (or, for the age-standardized death rates, a real
.csv) at a stable URL under https://www.ipss.go.jp/p-toukei/JMD/<AA>/STATS/ —
no auth, no pagination, no incremental query.

Each .txt file begins with a 1-line provenance title ("...Last modified:...")
then a blank line, then a column-header row, then whitespace-delimited data;
the Age column carries an open "110+" interval and missing numerics are ".".
These helpers are shared by every published subset's fetcher.
"""

import httpx

from subsets_utils import get, transient_retry

BASE = "https://www.ipss.go.jp/p-toukei/JMD"

# Area code -> human-readable name. 00 = All Japan, 01-47 = prefectures.
AREAS = {
    "00": "All Japan",
    "01": "Hokkaido", "02": "Aomori", "03": "Iwate", "04": "Miyagi",
    "05": "Akita", "06": "Yamagata", "07": "Fukushima", "08": "Ibaraki",
    "09": "Tochigi", "10": "Gunma", "11": "Saitama", "12": "Chiba",
    "13": "Tokyo", "14": "Kanagawa", "15": "Niigata", "16": "Toyama",
    "17": "Ishikawa", "18": "Fukui", "19": "Yamanashi", "20": "Nagano",
    "21": "Gifu", "22": "Shizuoka", "23": "Aichi", "24": "Mie",
    "25": "Shiga", "26": "Kyoto", "27": "Osaka", "28": "Hyogo",
    "29": "Nara", "30": "Wakayama", "31": "Tottori", "32": "Shimane",
    "33": "Okayama", "34": "Hiroshima", "35": "Yamaguchi", "36": "Tokushima",
    "37": "Kagawa", "38": "Ehime", "39": "Kochi", "40": "Fukuoka",
    "41": "Saga", "42": "Nagasaki", "43": "Kumamoto", "44": "Oita",
    "45": "Miyazaki", "46": "Kagoshima", "47": "Okinawa",
}


# ----------------------------------------------------------------------------
# HTTP with retry — transient (429/5xx/timeouts) retried, permanent surfaced.
# ----------------------------------------------------------------------------


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # JMD text files are ASCII/latin; force a sane decode.
    resp.encoding = resp.encoding or "utf-8"
    return resp.text


def _num(tok: str):
    """Parse a numeric token; JMD uses '.' for missing -> None."""
    if tok in (".", "", "NA", "na", "-"):
        return None
    try:
        return float(tok)
    except ValueError:
        return None


def _year(tok: str):
    """Year tokens are 4-digit; tolerate a trailing non-digit just in case."""
    try:
        return int(tok)
    except ValueError:
        digits = "".join(c for c in tok if c.isdigit())
        return int(digits[:4]) if len(digits) >= 4 else None


def _data_lines(text: str):
    """Yield post-header data lines: skip the title line, the blank line, and
    the column-header row (the first line whose first token is 'Year')."""
    seen_header = False
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        first = s.split()[0]
        if not seen_header:
            if first == "Year":
                seen_header = True
            continue
        yield s


def _iter_areas(filename: str):
    """Fetch `filename` for every area; yield (area_code, area_name, text).
    A per-area 404 (file genuinely absent for that prefecture) is skipped, not
    fatal — coverage across the rest of the corpus is preserved."""
    for code, name in AREAS.items():
        url = f"{BASE}/{code}/STATS/{filename}"
        try:
            text = _fetch_text(url)
        except httpx.HTTPStatusError as exc:
            sc = exc.response.status_code
            if sc == 404 or (400 <= sc < 500 and sc != 429):
                print(f"[ipss-japan] skip {url}: HTTP {sc} (absent for area)")
                continue
            raise
        yield code, name, text
