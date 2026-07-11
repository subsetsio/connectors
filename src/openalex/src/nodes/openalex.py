"""OpenAlex download specs.

The flattening code lives in one helper module per entity; this canonical
module is the single owner of DOWNLOAD_SPECS for the factory harness.
"""

from subsets_utils import NodeSpec

from nodes import concepts, domains, fields, funders, institutions, keywords
from nodes import publishers, sdgs, sources, subfields, topics
from nodes import works_by_dimension_year, works_by_year


def fetch_concepts(node_id: str) -> None:
    concepts.fetch(node_id)


def fetch_domains(node_id: str) -> None:
    domains.fetch(node_id)


def fetch_fields(node_id: str) -> None:
    fields.fetch(node_id)


def fetch_funders(node_id: str) -> None:
    funders.fetch(node_id)


def fetch_institutions(node_id: str) -> None:
    institutions.fetch(node_id)


def fetch_keywords(node_id: str) -> None:
    keywords.fetch(node_id)


def fetch_publishers(node_id: str) -> None:
    publishers.fetch(node_id)


def fetch_sdgs(node_id: str) -> None:
    sdgs.fetch(node_id)


def fetch_sources(node_id: str) -> None:
    sources.fetch(node_id)


def fetch_subfields(node_id: str) -> None:
    subfields.fetch(node_id)


def fetch_topics(node_id: str) -> None:
    topics.fetch(node_id)


def fetch_works_by_dimension_year(node_id: str) -> None:
    works_by_dimension_year.fetch(node_id)


def fetch_works_by_year(node_id: str) -> None:
    works_by_year.fetch(node_id)


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
