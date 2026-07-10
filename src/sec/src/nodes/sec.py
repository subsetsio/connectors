"""Download spec declarations for the SEC connector.

Fetch implementations are split by dataset for readability; this module is
the harness-facing declaration surface for the download stage.
"""
from subsets_utils import NodeSpec

from nodes.companies import fetch_companies
from nodes.concepts import fetch_concepts
from nodes.facts import fetch_facts


DOWNLOAD_SPECS = [
    NodeSpec(id="sec-companies", fn=fetch_companies, kind="download"),
    NodeSpec(id="sec-concepts", fn=fetch_concepts, kind="download"),
    NodeSpec(id="sec-facts", fn=fetch_facts, kind="download"),
]
