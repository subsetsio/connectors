"""IRS download node registry."""

from __future__ import annotations

from subsets_utils import NodeSpec

from nodes.corp_source_book import fetch_corp_source_book
from nodes.eo_bmf import fetch_bmf
from nodes.eo_financial import fetch_eo_financial
from nodes.income import fetch_income
from nodes.migration import fetch_migration


DOWNLOAD_SPECS = [
    NodeSpec(id="irs-corp-source-book", fn=fetch_corp_source_book, kind="download"),
    NodeSpec(id="irs-county-income", fn=fetch_income, kind="download"),
    NodeSpec(id="irs-county-migration", fn=fetch_migration, kind="download"),
    NodeSpec(id="irs-eo-bmf", fn=fetch_bmf, kind="download"),
    NodeSpec(id="irs-eo-financial-990", fn=fetch_eo_financial, kind="download"),
    NodeSpec(id="irs-eo-financial-990ez", fn=fetch_eo_financial, kind="download"),
    NodeSpec(id="irs-eo-financial-990pf", fn=fetch_eo_financial, kind="download"),
    NodeSpec(id="irs-state-migration", fn=fetch_migration, kind="download"),
    NodeSpec(id="irs-zipcode-income", fn=fetch_income, kind="download"),
]
