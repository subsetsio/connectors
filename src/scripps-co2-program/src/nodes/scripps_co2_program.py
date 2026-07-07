"""Scripps CO2 Program connector downloads.

The source is a static data site: catalog pages contain direct CSV/TXT links,
plus occasional ZIP bundles. We normalize each linked tabular file into a
single NDJSON stream with provenance fields and JSON-encoded raw row payloads.
Transforms can then type the heterogeneous Scripps layouts from observed raw.
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    save_raw_ndjson,
)

BASE_URL = "https://scrippsco2.ucsd.edu"
SPEC_PREFIX = "scripps-co2-program-"


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.hrefs.append(value)


ENTITY_PAGES = {
    "atmospheric-station-records": [
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/alert-nwt-canada/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/utqiagvik-alaska/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/station-p/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/la-jolla-pier-california/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/baja-california-sur-mexico/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/mauna-loa-observatory-hawaii/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/cape-kumukahi-hawaii/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/fanning-island/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/christmas-island/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/american-samoa/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/kermadec-islands/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/baring-head-new-zealand/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/palmer-station-antarctica/",
        f"{BASE_URL}/data/atmospheric-co2-data/sampling-station-records/south-pole/",
    ],
    "averaged-atmospheric-products": [
        f"{BASE_URL}/data/atmospheric-co2-data/averaged-products/",
        f"{BASE_URL}/data/atmospheric_co2/averaged_products.html",
    ],
    "campaign-atmospheric-records": [
        f"{BASE_URL}/data/atmospheric-co2-data/campaign-data/aircraft-campaign-data-1958-1961/",
        f"{BASE_URL}/data/atmospheric-co2-data/campaign-data/ship-ice-floe-campaign-data-1957-1984/",
    ],
    "ice-core-merged-products": [
        f"{BASE_URL}/data/atmospheric-co2-data/ice-core-merged-products/",
        f"{BASE_URL}/data/atmospheric_co2/icecore_merged_products.html",
    ],
    "primary-mauna-loa-record": [
        f"{BASE_URL}/data/primary-mauna-loa-co2-record/",
        f"{BASE_URL}/data/atmospheric_co2/primary_mlo_co2_record.html",
    ],
    "seawater-carbon-records": [
        f"{BASE_URL}/data/seawater-carbon-data/early-cruise-pco2/",
        f"{BASE_URL}/data/seawater-carbon-data/ocean-time-series-data/",
    ],
}

FALLBACK_URLS = {
    "averaged-atmospheric-products": [
        f"{BASE_URL}/assets/data/atmospheric/averages/mlo_spo_monthly_mean.csv",
        f"{BASE_URL}/assets/data/atmospheric/averages/mlo_spo_annual_mean.csv",
    ],
    "ice-core-merged-products": [
        f"{BASE_URL}/assets/data/atmospheric/merged_ice_core_mlo_spo/merged_ice_core_yearly.csv",
        f"{BASE_URL}/assets/data/atmospheric/merged_ice_core_mlo_spo/spline_merged_ice_core_yearly.csv",
    ],
    "primary-mauna-loa-record": [
        f"{BASE_URL}/assets/data/atmospheric/stations/in_situ_co2/monthly/monthly_in_situ_co2_mlo.csv",
    ],
}

DOWNLOAD_EXTENSIONS = (".csv", ".txt", ".dat", ".zip")


def _entity_from_node_id(node_id: str) -> str:
    if not node_id.startswith(SPEC_PREFIX):
        raise ValueError(f"unexpected node id: {node_id}")
    entity = node_id.removeprefix(SPEC_PREFIX)
    if entity not in ENTITY_PAGES:
        raise KeyError(f"no page mapping for entity {entity!r}")
    return entity


def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _download_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _links_from_page(page_url: str) -> list[str]:
    html = _fetch_text(page_url)
    parser = _LinkParser()
    parser.feed(html)
    out: list[str] = []
    for href in parser.hrefs:
        normalized = urljoin(page_url, href)
        path = urlparse(normalized).path.lower()
        if path.endswith(DOWNLOAD_EXTENSIONS):
            out.append(normalized)
    return out


def _discover_urls(entity: str) -> list[tuple[str | None, str]]:
    seen: set[str] = set()
    discovered: list[tuple[str | None, str]] = []
    for page_url in ENTITY_PAGES[entity]:
        try:
            urls = _links_from_page(page_url)
        except Exception:
            if page_url == ENTITY_PAGES[entity][-1]:
                raise
            continue
        for url in urls:
            if url not in seen:
                seen.add(url)
                discovered.append((page_url, url))

    for url in FALLBACK_URLS.get(entity, []):
        if url not in seen:
            seen.add(url)
            discovered.append((None, url))

    # Prefer individual tabular links when both page tables and "download all"
    # ZIP bundles are exposed; ZIPs are retained as fallback-only sources.
    tabular = [(page, url) for page, url in discovered if not url.lower().endswith(".zip")]
    return tabular or discovered


def _decode(content: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _looks_like_header(fields: list[str]) -> bool:
    nonempty = [f.strip() for f in fields if f.strip()]
    if len(nonempty) < 2:
        return False
    alpha = sum(1 for f in nonempty if re.search(r"[A-Za-z]", f))
    numeric = sum(1 for f in nonempty if re.fullmatch(r"[-+]?\d+(\.\d+)?", f))
    return alpha >= 2 and numeric == 0


def _clean_header(fields: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: dict[str, int] = {}
    for index, field in enumerate(fields):
        base = re.sub(r"[^0-9A-Za-z]+", "_", field.strip().lower()).strip("_")
        name = base or f"column_{index + 1}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 1
        cleaned.append(name)
    return cleaned


def _rows_from_text(
    *,
    text: str,
    entity: str,
    source_url: str,
    source_page_url: str | None,
    inner_file: str | None = None,
) -> list[dict]:
    comments: list[str] = []
    data_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            comments.append(stripped.lstrip("#").strip())
        else:
            data_lines.append(line)

    reader = csv.reader(data_lines)
    rows = list(reader)
    if not rows:
        return []

    header: list[str] | None = None
    start = 0
    if _looks_like_header(rows[0]):
        header = _clean_header(rows[0])
        start = 1

    source_file = inner_file or urlparse(source_url).path.rsplit("/", 1)[-1]
    parsed: list[dict] = []
    for offset, fields in enumerate(rows[start:], start=1):
        values = {}
        if header:
            values = {name: fields[i] if i < len(fields) else None for i, name in enumerate(header)}
        parsed.append(
            {
                "entity_id": entity.replace("-", "_"),
                "source_page_url": source_page_url,
                "source_url": source_url,
                "source_file": source_file,
                "raw_row_number": offset,
                "raw_fields_json": json.dumps(fields, ensure_ascii=False),
                "columns_json": json.dumps(values, ensure_ascii=False),
                "comments_json": json.dumps(comments, ensure_ascii=False),
            }
        )
    return parsed


def _rows_from_url(entity: str, page_url: str | None, url: str) -> list[dict]:
    content = _download_bytes(url)
    if url.lower().endswith(".zip"):
        rows: list[dict] = []
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            for name in sorted(zf.namelist()):
                lower = name.lower()
                if lower.endswith((".csv", ".txt", ".dat")) and not name.endswith("/"):
                    rows.extend(
                        _rows_from_text(
                            text=_decode(zf.read(name)),
                            entity=entity,
                            source_url=url,
                            source_page_url=page_url,
                            inner_file=name,
                        )
                    )
        return rows

    return _rows_from_text(
        text=_decode(content),
        entity=entity,
        source_url=url,
        source_page_url=page_url,
    )


def fetch_entity(node_id: str) -> None:
    entity = _entity_from_node_id(node_id)
    rows: list[dict] = []
    source_urls = _discover_urls(entity)
    if not source_urls:
        raise RuntimeError(f"{entity}: no downloadable CSV/TXT/ZIP links discovered")

    for page_url, url in source_urls:
        rows.extend(_rows_from_url(entity, page_url, url))

    if not rows:
        raise RuntimeError(f"{entity}: discovered {len(source_urls)} files but parsed 0 rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="scripps-co2-program-atmospheric-station-records", fn=fetch_entity, kind="download"),
    NodeSpec(id="scripps-co2-program-averaged-atmospheric-products", fn=fetch_entity, kind="download"),
    NodeSpec(id="scripps-co2-program-campaign-atmospheric-records", fn=fetch_entity, kind="download"),
    NodeSpec(id="scripps-co2-program-ice-core-merged-products", fn=fetch_entity, kind="download"),
    NodeSpec(id="scripps-co2-program-primary-mauna-loa-record", fn=fetch_entity, kind="download"),
    NodeSpec(id="scripps-co2-program-seawater-carbon-records", fn=fetch_entity, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Full refresh; source notes data may be revised after recalibration "
            "and no explicit release cadence is published."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.zst", max_age_days=7),
    )
    for spec in DOWNLOAD_SPECS
]
