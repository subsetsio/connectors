-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "TABLE_IDENTIFIER" AS table_identifier,
    "FREQ" AS freq,
    "REF_AREA" AS ref_area,
    "COUNTERPART_AREA" AS counterpart_area,
    "ACTIVITY" AS activity,
    "NUMBER_EMPL" AS number_empl,
    "TOP_ENTERPRISES" AS top_enterprises,
    "NUMBER_PARTNERS" AS number_partners,
    "PRODUCT" AS product,
    "TRADE_POPULATION" AS trade_population,
    "FLOW" AS flow,
    "TYPE_CONTROL" AS type_control,
    "TYPE_TRADER" AS type_trader,
    "EXPORTS_INTENSITY" AS exports_intensity,
    "INDICATOR" AS indicator,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "CONF_STATUS" AS conf_status,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "UNIT_MEASURE" AS unit_measure,
    "EMBARGO_TIME" AS embargo_time
FROM "national-bank-of-belgium-df-extt-tec-country-activity"
