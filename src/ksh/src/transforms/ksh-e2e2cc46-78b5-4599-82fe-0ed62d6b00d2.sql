-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "ADJUSTMENT" AS adjustment,
    "REF_AREA" AS ref_area,
    "COUNTERPART_AREA" AS counterpart_area,
    "REF_SECTOR" AS ref_sector,
    "COUNTERPART_SECTOR" AS counterpart_sector,
    "ACCOUNTING_ENTRY" AS accounting_entry,
    "STO" AS sto,
    "INSTR_ASSET" AS instr_asset,
    "ACTIVITY" AS activity,
    "EXPENDITURE" AS expenditure,
    "UNIT_MEASURE" AS unit_measure,
    "PRICES" AS prices,
    "TRANSFORMATION" AS transformation,
    "REF_PERIOD_DETAIL" AS ref_period_detail,
    "TIME_FORMAT" AS time_format,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TABLE_IDENTIFIER" AS table_identifier,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "LAST_UPDATE" AS last_update,
    "COMMENT_TS" AS comment_ts,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "CONF_STATUS" AS conf_status,
    "EMBARGO_DATE" AS embargo_date
FROM "ksh-e2e2cc46-78b5-4599-82fe-0ed62d6b00d2"
