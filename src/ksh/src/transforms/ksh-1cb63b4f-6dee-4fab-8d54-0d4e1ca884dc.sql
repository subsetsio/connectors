-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "REF_AREA" AS ref_area,
    "COUNTERPART_AREA" AS counterpart_area,
    "REF_SECTOR" AS ref_sector,
    "COUNTERPART_SECTOR" AS counterpart_sector,
    "ACCOUNTING_ENTRY" AS accounting_entry,
    "STO" AS sto,
    "ACTIVITY" AS activity,
    "VALUATION" AS valuation,
    "PRICES" AS prices,
    "UNIT_MEASURE" AS unit_measure,
    "TRANSFORMATION" AS transformation,
    "REF_PERIOD_DETAIL" AS ref_period_detail,
    "TIME_FORMAT" AS time_format,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TABLE_IDENTIFIER" AS table_identifier,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "LAST_UPDATE" AS last_update,
    "COMMENT_TS" AS comment_ts,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status,
    "CONF_STATUS" AS conf_status,
    "EMBARGO_DATE" AS embargo_date
FROM "ksh-1cb63b4f-6dee-4fab-8d54-0d4e1ca884dc"
