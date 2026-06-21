"""Shared helpers for the Gapminder connector.

Source: Gapminder's DDF-csv fact-base, published in the open-numbers GitHub org
(repos ddf--gapminder--systema_globalis and ddf--gapminder--fasttrack). The
ddf--gapminder--wdi repo is a verbatim World Bank copy and is intentionally
excluded (redundant with the world-bank connector).
"""
from subsets_utils import get, transient_retry

REPOS = {
    "systema_globalis": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master",
    "fasttrack": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--fasttrack/master",
}


@transient_retry(min_wait=2, max_wait=60)
def get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry(min_wait=2, max_wait=60)
def get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()
