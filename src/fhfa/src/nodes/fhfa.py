"""FHFA download specs.

Fetch implementations are split by product for readability. The harness
expects the public download specs and their callables to live in this slug-named
module, so the functions below are top-level wrappers around the product
modules.
"""

from subsets_utils import NodeSpec

from nodes.conforming_loan_limits import fetch_conforming_loan_limits as _fetch_conforming_loan_limits
from nodes.duty_to_serve import fetch_duty_to_serve as _fetch_duty_to_serve
from nodes.enterprise_housing_goals import fetch_enterprise_housing_goals as _fetch_enterprise_housing_goals
from nodes.fhlb_member_data import fetch_fhlb_member_data as _fetch_fhlb_member_data
from nodes.hpi import fetch_hpi as _fetch_hpi
from nodes.mirs_transition_index import fetch_mirs_transition_index as _fetch_mirs_transition_index
from nodes.nmdb_aggregate_statistics import fetch_nmdb_aggregate_statistics as _fetch_nmdb_aggregate_statistics
from nodes.pudb_enterprise_multifamily import fetch_pudb_enterprise_multifamily as _fetch_pudb_enterprise_multifamily
from nodes.pudb_enterprise_single_family import fetch_pudb_enterprise_single_family as _fetch_pudb_enterprise_single_family
from nodes.pudb_fhlbank import fetch_pudb_fhlbank as _fetch_pudb_fhlbank
from nodes.uad_aggregate_statistics import fetch_uad_aggregate_statistics as _fetch_uad_aggregate_statistics
from nodes.underserved_areas_data import fetch_underserved_areas_data as _fetch_underserved_areas_data


def fetch_conforming_loan_limits(node_id: str) -> None:
    _fetch_conforming_loan_limits(node_id)


def fetch_duty_to_serve(node_id: str) -> None:
    _fetch_duty_to_serve(node_id)


def fetch_enterprise_housing_goals(node_id: str) -> None:
    _fetch_enterprise_housing_goals(node_id)


def fetch_fhlb_member_data(node_id: str) -> None:
    _fetch_fhlb_member_data(node_id)


def fetch_hpi(node_id: str) -> None:
    _fetch_hpi(node_id)


def fetch_mirs_transition_index(node_id: str) -> None:
    _fetch_mirs_transition_index(node_id)


def fetch_nmdb_aggregate_statistics(node_id: str) -> None:
    _fetch_nmdb_aggregate_statistics(node_id)


def fetch_pudb_enterprise_multifamily(node_id: str) -> None:
    _fetch_pudb_enterprise_multifamily(node_id)


def fetch_pudb_enterprise_single_family(node_id: str) -> None:
    _fetch_pudb_enterprise_single_family(node_id)


def fetch_pudb_fhlbank(node_id: str) -> None:
    _fetch_pudb_fhlbank(node_id)


def fetch_uad_aggregate_statistics(node_id: str) -> None:
    _fetch_uad_aggregate_statistics(node_id)


def fetch_underserved_areas_data(node_id: str) -> None:
    _fetch_underserved_areas_data(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-conforming-loan-limits", fn=fetch_conforming_loan_limits, kind="download"),
    NodeSpec(id="fhfa-duty-to-serve", fn=fetch_duty_to_serve, kind="download"),
    NodeSpec(id="fhfa-enterprise-housing-goals", fn=fetch_enterprise_housing_goals, kind="download"),
    NodeSpec(id="fhfa-fhlbank-member-data", fn=fetch_fhlb_member_data, kind="download"),
    NodeSpec(id="fhfa-hpi", fn=fetch_hpi, kind="download"),
    NodeSpec(id="fhfa-mirs-transition-index", fn=fetch_mirs_transition_index, kind="download"),
    NodeSpec(id="fhfa-nmdb-aggregate-statistics", fn=fetch_nmdb_aggregate_statistics, kind="download"),
    NodeSpec(id="fhfa-pudb-enterprise-multifamily", fn=fetch_pudb_enterprise_multifamily, kind="download"),
    NodeSpec(id="fhfa-pudb-enterprise-single-family", fn=fetch_pudb_enterprise_single_family, kind="download"),
    NodeSpec(id="fhfa-pudb-fhlbank", fn=fetch_pudb_fhlbank, kind="download"),
    NodeSpec(id="fhfa-uad-aggregate-statistics", fn=fetch_uad_aggregate_statistics, kind="download"),
    NodeSpec(id="fhfa-underserved-areas-data", fn=fetch_underserved_areas_data, kind="download"),
]
