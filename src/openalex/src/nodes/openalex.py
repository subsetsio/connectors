"""OpenAlex download specs.

The flattening code lives in one helper module per entity; this canonical
module is the single owner of DOWNLOAD_SPECS for the factory harness.
"""

from subsets_utils import NodeSpec

from nodes.concepts import fetch as fetch_concepts
from nodes.domains import fetch as fetch_domains
from nodes.fields import fetch as fetch_fields
from nodes.funders import fetch as fetch_funders
from nodes.institutions import fetch as fetch_institutions
from nodes.keywords import fetch as fetch_keywords
from nodes.publishers import fetch as fetch_publishers
from nodes.sdgs import fetch as fetch_sdgs
from nodes.sources import fetch as fetch_sources
from nodes.subfields import fetch as fetch_subfields
from nodes.topics import fetch as fetch_topics
from nodes.works_by_dimension_year import fetch as fetch_works_by_dimension_year
from nodes.works_by_year import fetch as fetch_works_by_year


DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-concepts", fn=fetch_concepts, kind="download"),
    NodeSpec(id="openalex-domains", fn=fetch_domains, kind="download"),
    NodeSpec(id="openalex-fields", fn=fetch_fields, kind="download"),
    NodeSpec(id="openalex-funders", fn=fetch_funders, kind="download"),
    NodeSpec(id="openalex-institutions", fn=fetch_institutions, kind="download"),
    NodeSpec(id="openalex-keywords", fn=fetch_keywords, kind="download"),
    NodeSpec(id="openalex-publishers", fn=fetch_publishers, kind="download"),
    NodeSpec(id="openalex-sdgs", fn=fetch_sdgs, kind="download"),
    NodeSpec(id="openalex-sources", fn=fetch_sources, kind="download"),
    NodeSpec(id="openalex-subfields", fn=fetch_subfields, kind="download"),
    NodeSpec(id="openalex-topics", fn=fetch_topics, kind="download"),
    NodeSpec(id="openalex-works-by-dimension-year", fn=fetch_works_by_dimension_year, kind="download"),
    NodeSpec(id="openalex-works-by-year", fn=fetch_works_by_year, kind="download"),
]
