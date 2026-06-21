"""npm-security-advisories — advisories affecting each package's published versions.

No incremental query support on the advisory endpoint, so the package head is
re-fetched in full every run.
"""
from urllib.parse import quote

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import REGISTRY_URL, _get_resp, _post_json, _popular_names

ADVISORIES_BULK = "https://registry.npmjs.org/-/npm/v1/security/advisories/bulk"
ADVISORY_BATCH = 100        # packages per bulk-advisory POST
# Abbreviated packument: lists every version cheaply (~tens of KB vs multi-MB).
_ABBREV_HEADERS = {"Accept": "application/vnd.npm.install-v1+json"}

_ADVISORIES_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("advisory_id", pa.int64()),
    ("url", pa.string()),
    ("title", pa.string()),
    ("severity", pa.string()),
    ("vulnerable_versions", pa.string()),
    ("cwe", pa.list_(pa.string())),
    ("cvss_score", pa.float64()),
    ("cvss_vector", pa.string()),
])


def _all_versions(name: str) -> list[str]:
    """Every published version of a package, via the abbreviated packument."""
    resp = _get_resp(f"{REGISTRY_URL}/{quote(name, safe='@/')}", headers=_ABBREV_HEADERS)
    if resp is None:
        return []
    return list((resp.json().get("versions") or {}).keys())


def fetch_security_advisories(node_id: str) -> None:
    """Known advisories affecting ANY published version of each popular package.

    Querying only the latest version finds almost nothing (popular packages keep
    their latest release patched), so we submit each package's full version list
    to the bulk endpoint, which returns every advisory whose range intersects.
    """
    names = _popular_names()
    print(f"  {node_id}: collecting version lists for {len(names):,} packages")

    rows: list[dict] = []
    for i in range(0, len(names), ADVISORY_BATCH):
        batch = names[i:i + ADVISORY_BATCH]
        payload = {}
        for n in batch:
            vers = _all_versions(n)
            if vers:
                payload[n] = vers
        if not payload:
            continue
        data = _post_json(ADVISORIES_BULK, payload)
        for pkg, advisories in data.items():
            seen_ids = set()
            for adv in advisories or []:
                aid = int(adv["id"])
                if aid in seen_ids:
                    continue
                seen_ids.add(aid)
                cvss = adv.get("cvss") or {}
                rows.append({
                    "package": pkg,
                    "advisory_id": aid,
                    "url": adv.get("url"),
                    "title": adv.get("title"),
                    "severity": adv.get("severity"),
                    "vulnerable_versions": adv.get("vulnerable_versions"),
                    "cwe": adv.get("cwe") or [],
                    "cvss_score": float(cvss["score"]) if cvss.get("score") is not None else None,
                    "cvss_vector": cvss.get("vectorString"),
                })
        print(f"    {min(i + ADVISORY_BATCH, len(names)):,}/{len(names):,} packages ({len(rows):,} advisory rows)")
    table = pa.Table.from_pylist(rows, schema=_ADVISORIES_SCHEMA)
    save_raw_parquet(table, node_id)
    print(f"  {node_id}: {table.num_rows:,} advisory rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="npm-security-advisories", fn=fetch_security_advisories, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="npm-security-advisories-transform",
        deps=["npm-security-advisories"],
        sql='''
            SELECT
                package,
                CAST(advisory_id AS BIGINT) AS advisory_id,
                url,
                title,
                severity,
                vulnerable_versions,
                cwe,
                CAST(cvss_score AS DOUBLE)  AS cvss_score,
                cvss_vector
            FROM "npm-security-advisories"
            WHERE package IS NOT NULL AND advisory_id IS NOT NULL
        ''',
    ),
]
