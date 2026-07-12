"""Canonical download specs for the crates.io connector."""

from subsets_utils import NodeSpec

from nodes.categories import fetch_categories
from nodes.crate_categories import fetch_crate_categories
from nodes.crate_keywords import fetch_crate_keywords
from nodes.crates import fetch_crates
from nodes.dependencies import fetch_dependencies
from nodes.keywords import fetch_keywords
from nodes.version_downloads_daily import fetch_version_downloads
from nodes.versions import fetch_versions


DOWNLOAD_SPECS = [
    NodeSpec(id="crates-io-categories", fn=fetch_categories, kind="download"),
    NodeSpec(id="crates-io-crate-categories", fn=fetch_crate_categories, kind="download"),
    NodeSpec(id="crates-io-crate-keywords", fn=fetch_crate_keywords, kind="download"),
    NodeSpec(id="crates-io-crates", fn=fetch_crates, kind="download"),
    NodeSpec(id="crates-io-dependencies", fn=fetch_dependencies, kind="download"),
    NodeSpec(id="crates-io-keywords", fn=fetch_keywords, kind="download"),
    NodeSpec(
        id="crates-io-version-downloads-daily",
        fn=fetch_version_downloads,
        kind="download",
    ),
    NodeSpec(id="crates-io-versions", fn=fetch_versions, kind="download"),
]
