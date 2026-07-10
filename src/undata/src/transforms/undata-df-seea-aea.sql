-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Air emission accounts contain multiple accounting entries, sectors, products, and counterpart areas; filter those dimensions before summing observations.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "REF_AREA" AS ref_area,
    "DEMAND_PROD" AS demand_prod,
    "ACCOUNTING_ENTRY" AS accounting_entry,
    "COUNTERPART_AREA" AS counterpart_area,
    "INTERACTORS" AS interactors,
    "BRIDGE_ITEMS" AS bridge_items,
    "AIRPOL" AS airpol,
    "STO" AS sto,
    "UNIT_MEASURE" AS unit_measure,
    "PRODUCT" AS product,
    "SECTOR" AS sector,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "DISS_ORG" AS diss_org,
    "PRE_BREAK_VALUE" AS pre_break_value,
    "COMPILING_ORG" AS compiling_org,
    "LAST_UPDATE" AS last_update,
    "TITLE_COMPL" AS title_compl,
    "TITLE" AS title,
    "DECIMALS" AS decimals,
    "EMBARGO_TIME" AS embargo_time,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "COMMENT_TS" AS comment_ts,
    "COMMENT_OBS" AS comment_obs,
    "COMMENT_DSET" AS comment_dset,
    "OBS_STATUS_4" AS obs_status_4,
    "OBS_STATUS_3" AS obs_status_3,
    "OBS_STATUS_2" AS obs_status_2,
    "OBS_STATUS_1" AS obs_status_1,
    "CONF_STATUS" AS conf_status
FROM "undata-df-seea-aea"
