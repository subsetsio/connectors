"""Data.gov download specs."""

from subsets_utils import NodeSpec

from nodes.datasets import fetch_datasets
from nodes.groups import fetch_groups
from nodes.organizations import fetch_organizations
from nodes.resources import fetch_resources


DOWNLOAD_SPECS = [
    NodeSpec(id="data-gov-datasets", fn=fetch_datasets, kind="download"),
    NodeSpec(id="data-gov-groups", fn=fetch_groups, kind="download"),
    NodeSpec(id="data-gov-organizations", fn=fetch_organizations, kind="download"),
    NodeSpec(id="data-gov-resources", fn=fetch_resources, kind="download"),
]
