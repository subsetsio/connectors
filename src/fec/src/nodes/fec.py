"""Download spec registry for the FEC bulk-data connector."""

from __future__ import annotations

from subsets_utils import NodeSpec

from nodes.candidate_committee_linkages import fetch_linkages
from nodes.candidates import fetch_candidates
from nodes.committees import fetch_committees
from nodes.house_senate_current_campaigns import fetch_house_senate
from nodes.independent_expenditures import fetch_independent_expenditures
from nodes.individual_contributions import fetch_individual_contributions
from nodes.inter_committee_transactions import fetch_inter_committee
from nodes.operating_expenditures import fetch_operating_expenditures
from nodes.pac_contributions import fetch_pac_contributions


DOWNLOAD_SPECS = [
    NodeSpec(id="fec-candidate-committee-linkages", fn=fetch_linkages, kind="download"),
    NodeSpec(id="fec-candidates", fn=fetch_candidates, kind="download"),
    NodeSpec(id="fec-committees", fn=fetch_committees, kind="download"),
    NodeSpec(id="fec-house-senate-current-campaigns", fn=fetch_house_senate, kind="download"),
    NodeSpec(id="fec-independent-expenditures", fn=fetch_independent_expenditures, kind="download"),
    NodeSpec(id="fec-individual-contributions", fn=fetch_individual_contributions, kind="download"),
    NodeSpec(id="fec-inter-committee-transactions", fn=fetch_inter_committee, kind="download"),
    NodeSpec(id="fec-operating-expenditures", fn=fetch_operating_expenditures, kind="download"),
    NodeSpec(id="fec-pac-contributions", fn=fetch_pac_contributions, kind="download"),
]
