"""Bioconductor connector.

Two subsets, both stateless full re-pulls (the whole corpus is a handful of
bulk files fetched in seconds):

- ``downloads`` — monthly package download time-series. One TSV per package
  repository (bioc / data-experiment / data-annotation / workflows) at the
  stable URL ``/packages/stats/<repo>/<stem>_pkg_stats.tab``; the four share an
  identical schema so they union into one long table via a ``repo`` column.
  Columns upstream: Package, Year, Month (3-letter abbr, plus a synthetic
  Month='all' annual-total row per package-year), Nb_of_distinct_IPs,
  Nb_of_downloads. This is the connector's primary statistical product.

- ``packages`` — the package-metadata catalog (release VIEWS, DCF format), one
  row per package across all four repositories. Reference / dimension table,
  joinable to ``downloads`` on (package, repo).

No incremental query exists for either; both files are full snapshots, so we
re-fetch and overwrite each refresh (the maintain step gates cadence). No auth,
no documented rate limit.

NOTE (2026-06): the .tab stats files are in a transient 404 outage from the
Bioconductor website migration (status.bioconductor.org tracked it as
"Package Stats Failed Check"). The canonical URLs and TSV schema are correct
and were live through mid-May 2026; a 404 here is the outage, not a URL change,
and the download node will fail loudly until the source restores the files.
"""

import csv
import io

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# repo slug (also the `repo` column value) -> (stats path segment, file stem)
STATS_REPOS = {
    "bioc": ("bioc", "bioc"),
    "data-experiment": ("data-experiment", "experiment"),
    "data-annotation": ("data-annotation", "annotation"),
    "workflows": ("workflows", "workflows"),
}

# repo slug -> release VIEWS path segment
VIEWS_REPOS = {
    "bioc": "bioc",
    "data-experiment": "data/experiment",
    "data-annotation": "data/annotation",
    "workflows": "workflows",
}

DOWNLOADS_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("repo", pa.string()),
    ("year", pa.int32()),
    ("month", pa.string()),          # 'Jan'..'Dec' or 'all' (annual total) — kept verbatim
    ("distinct_ips", pa.int64()),
    ("downloads", pa.int64()),
])

# DCF field name (as it appears in VIEWS) -> output column name. All textual.
PACKAGE_FIELDS = {
    "Package": "package",
    "Version": "version",
    "Title": "title",
    "Description": "description",
    "biocViews": "biocviews",
    "License": "license",
    "Maintainer": "maintainer",
    "Depends": "depends",
    "Imports": "imports",
    "NeedsCompilation": "needs_compilation",
    "git_last_commit_date": "git_last_commit_date",
    "Date/Publication": "date_publication",
}

PACKAGES_SCHEMA = pa.schema([(col, pa.string()) for col in
                             ["repo"] + list(PACKAGE_FIELDS.values())])


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()  # 404 during the migration outage raises here (not transient)
    return resp.text


def fetch_downloads(node_id: str) -> None:
    asset = node_id
    rows = []
    for repo, (seg, stem) in STATS_REPOS.items():
        url = f"https://bioconductor.org/packages/stats/{seg}/{stem}_pkg_stats.tab"
        text = _fetch_text(url)
        reader = csv.DictReader(io.StringIO(text), delimiter="\t")
        for rec in reader:
            rows.append({
                "package": rec["Package"],
                "repo": repo,
                "year": int(rec["Year"]),
                "month": rec["Month"],
                "distinct_ips": int(rec["Nb_of_distinct_IPs"]),
                "downloads": int(rec["Nb_of_downloads"]),
            })
    table = pa.Table.from_pylist(rows, schema=DOWNLOADS_SCHEMA)
    save_raw_parquet(table, asset)


def _parse_dcf(text: str):
    """Yield one dict per DCF record (blank-line separated, indented
    continuation lines fold into the prior field)."""
    record = {}
    key = None
    for line in text.splitlines():
        if not line.strip():
            if record:
                yield record
            record, key = {}, None
            continue
        if line[:1] in (" ", "\t"):  # continuation of the previous field
            if key is not None:
                record[key] = (record[key] + " " + line.strip()).strip()
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            key = k.strip()
            record[key] = v.strip()
    if record:
        yield record


def fetch_packages(node_id: str) -> None:
    asset = node_id
    rows = []
    for repo, seg in VIEWS_REPOS.items():
        text = _fetch_text(f"https://bioconductor.org/packages/release/{seg}/VIEWS")
        for rec in _parse_dcf(text):
            if "Package" not in rec:
                continue
            row = {"repo": repo}
            for src, col in PACKAGE_FIELDS.items():
                row[col] = rec.get(src)
            rows.append(row)
    table = pa.Table.from_pylist(rows, schema=PACKAGES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="bioconductor-downloads", fn=fetch_downloads, kind="download"),
    NodeSpec(id="bioconductor-packages", fn=fetch_packages, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bioconductor-downloads-transform",
        deps=["bioconductor-downloads"],
        sql='''
            SELECT
                make_date(CAST(year AS INTEGER), m.month_num, 1) AS date,
                package,
                repo,
                CAST(year AS INTEGER)         AS year,
                m.month_num                   AS month,
                CAST(distinct_ips AS BIGINT)  AS distinct_ips,
                CAST(downloads AS BIGINT)     AS downloads
            FROM "bioconductor-downloads"
            JOIN (VALUES
                ('Jan', 1), ('Feb', 2), ('Mar', 3), ('Apr', 4),
                ('May', 5), ('Jun', 6), ('Jul', 7), ('Aug', 8),
                ('Sep', 9), ('Oct', 10), ('Nov', 11), ('Dec', 12)
            ) AS m(month_abbr, month_num) ON month = m.month_abbr
        ''',
    ),
    SqlNodeSpec(
        id="bioconductor-packages-transform",
        deps=["bioconductor-packages"],
        sql='''
            SELECT
                package,
                repo,
                version,
                title,
                description,
                biocviews,
                license,
                maintainer,
                depends,
                imports,
                needs_compilation,
                TRY_CAST(git_last_commit_date AS DATE) AS git_last_commit_date,
                TRY_CAST(date_publication AS DATE)     AS date_publication
            FROM "bioconductor-packages"
        ''',
    ),
]
