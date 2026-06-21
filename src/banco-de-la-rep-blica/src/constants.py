# Entity union — Banco de la República SDMX dataflows (agency ESTAT, *_HIST
# variants ranked at/above the publish threshold). Copied verbatim from
# data/sources/banco-de-la-rep-blica/work/entity_union.json.
#
# Three source dataflows were dropped as exact duplicates (identical series,
# row count and observations) of a higher-ranked sibling and demoted below the
# publish threshold at rank: DF_DTF_HIST (== DF_DTF_DAILY_HIST),
# DF_FTD_MONTHLY_HIST (== DF_DTF_MONTHLY_HIST), DF_IBR_HIST (== DF_IBR_DAILY_HIST).
ENTITY_IDS = [
    "DF_CBR_DAILY_HIST",
    "DF_CBR_MONTHLY_HIST",
    "DF_COLCAP_MONTHLY_HIST",
    "DF_DTF_DAILY_HIST",
    "DF_DTF_MONTHLY_HIST",
    "DF_DTF_TRIM_ANTICIPADO_HIST",
    "DF_IBR_DAILY_HIST",
    "DF_IR_DAILY_HIST",
    "DF_IR_MONTHLY_HIST",
    "DF_MONAGG_MONTHLY_HIST",
    "DF_TES_MONTHLY_HIST",
    "DF_TRM_DAILY_HIST",
    "DF_UVR_DAILY_HIST",
]
