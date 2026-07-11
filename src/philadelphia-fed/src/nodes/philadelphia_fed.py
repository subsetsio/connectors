"""Public download spec surface for the Philadelphia Fed connector."""

from subsets_utils import NodeSpec

from nodes.ads_business_conditions import fetch_ads_business_conditions
from nodes.atsix import fetch_atsix
from nodes.gdpplus import fetch_gdpplus
from nodes.livingston_survey import fetch_livingston_survey
from nodes.manufacturing_business_outlook_survey import fetch_manufacturing_business_outlook_survey
from nodes.nonmanufacturing_business_outlook_survey import fetch_nonmanufacturing_business_outlook_survey
from nodes.partisan_conflict_index import fetch_partisan_conflict_index
from nodes.real_time_data_set_macroeconomists import fetch_real_time_data_set_macroeconomists
from nodes.spf_anxious_index import fetch_spf_anxious_index
from nodes.spf_consensus import fetch_spf_consensus
from nodes.spf_dispersion import fetch_spf_dispersion
from nodes.spf_error_statistics import fetch_spf_error_statistics
from nodes.state_coincident_indexes import fetch_state_coincident_indexes

DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-ads-business-conditions", fn=fetch_ads_business_conditions, kind="download"),
    NodeSpec(id="philadelphia-fed-atsix", fn=fetch_atsix, kind="download"),
    NodeSpec(id="philadelphia-fed-gdpplus", fn=fetch_gdpplus, kind="download"),
    NodeSpec(id="philadelphia-fed-livingston-survey", fn=fetch_livingston_survey, kind="download"),
    NodeSpec(id="philadelphia-fed-manufacturing-business-outlook-survey", fn=fetch_manufacturing_business_outlook_survey, kind="download"),
    NodeSpec(id="philadelphia-fed-nonmanufacturing-business-outlook-survey", fn=fetch_nonmanufacturing_business_outlook_survey, kind="download"),
    NodeSpec(id="philadelphia-fed-partisan-conflict-index", fn=fetch_partisan_conflict_index, kind="download"),
    NodeSpec(id="philadelphia-fed-real-time-data-set-macroeconomists", fn=fetch_real_time_data_set_macroeconomists, kind="download"),
    NodeSpec(id="philadelphia-fed-spf-anxious-index", fn=fetch_spf_anxious_index, kind="download"),
    NodeSpec(id="philadelphia-fed-spf-consensus", fn=fetch_spf_consensus, kind="download"),
    NodeSpec(id="philadelphia-fed-spf-dispersion", fn=fetch_spf_dispersion, kind="download"),
    NodeSpec(id="philadelphia-fed-spf-error-statistics", fn=fetch_spf_error_statistics, kind="download"),
    NodeSpec(id="philadelphia-fed-state-coincident-indexes", fn=fetch_state_coincident_indexes, kind="download"),
]
