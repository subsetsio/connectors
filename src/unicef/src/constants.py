"""Dataset-id selections for the unicef connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "BRAZIL_CO:BRAZIL_CO:1.0",
    "BRAZIL_CO:BRAZIL_CO_SELO:1.0",
    "CAP2030:CAP2030:1.0",
    "ECARO:ECACID:1.0",
    "ECARO:TRANSMONEE:1.0",
    "MENARO:MENARO:1.0",
    "PCO:PAKISTAN_CO:1.0",
    "UNICEF:CAUSE_OF_DEATH:1.0",
    "UNICEF:CCRI:1.0",
    "UNICEF:CHILD_RELATED_SDG:1.0",
    "UNICEF:CHLD_PVTY:1.0",
    "UNICEF:CME:1.0",
    "UNICEF:CME_CAUSE_OF_DEATH:1.0",
    "UNICEF:CME_COUNTRY_PROFILES_DATA:1.0",
    "UNICEF:CME_DF_2021_WQ:1.0",
    "UNICEF:CME_SUBNATIONAL:1.0",
    "UNICEF:DM:1.0",
    "UNICEF:DM_PROJECTIONS:1.0",
    "UNICEF:ECD:1.0",
    "UNICEF:ECONOMIC:1.0",
    "UNICEF:EDUCATION:1.0",
    "UNICEF:EDUCATION_FLS:1.0",
    "UNICEF:EDUCATION_LG:1.0",
    "UNICEF:EDUCATION_UIS_SDG:1.0",
    "UNICEF:FUNCTIONAL_DIFF:1.0",
    "UNICEF:GENDER:1.0",
    "UNICEF:GLOBAL_DATAFLOW:1.0",
    "UNICEF:HIV_AIDS:1.0",
    "UNICEF:IMMUNISATION:1.0",
    "UNICEF:MG:1.0",
    "UNICEF:MG_FLOW:1.0",
    "UNICEF:MNCH:1.0",
    "UNICEF:NUTRITION:1.0",
    "UNICEF:PT:1.0",
    "UNICEF:PT_CM:1.0",
    "UNICEF:PT_CM_SUBNATIONAL:1.0",
    "UNICEF:PT_CONFLICT:1.0",
    "UNICEF:PT_FGM:1.0",
    "UNICEF:SDG_PROG_ASSESSMENT:1.1",
    "UNICEF:SOC_PROTECTION:1.0",
    "UNICEF:WASH_HEALTHCARE_FACILITY:1.0",
    "UNICEF:WASH_HOUSEHOLDS:1.0",
    "UNICEF:WASH_HOUSEHOLD_MH:1.0",
    "UNICEF:WASH_HOUSEHOLD_SUBNAT:1.0",
    "UNICEF:WASH_SCHOOLS:1.0",
    "UNICEF:WT:1.0",
    "UNPD:UNPD_DEMOGRAPHY:1.0",
    "UNPD:UNPD_DM_PROJECTIONS:1.0",
]
