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
    "CONSOLIDATION" AS consolidation,
    "ACCOUNTING_ENTRY" AS accounting_entry,
    "STO" AS sto,
    "INSTR_ASSET" AS instr_asset,
    "MATURITY" AS maturity,
    "EXPENDITURE" AS expenditure,
    "UNIT_MEASURE" AS unit_measure,
    "CURRENCY_DENOM" AS currency_denom,
    "VALUATION" AS valuation,
    "PRICES" AS prices,
    "TRANSFORMATION" AS transformation,
    "CUST_BREAKDOWN" AS cust_breakdown,
    "REF_PERIOD_DETAIL" AS ref_period_detail,
    "TIME_FORMAT" AS time_format,
    "CUST_BREAKDOWN_LB" AS cust_breakdown_lb,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TABLE_IDENTIFIER" AS table_identifier,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "LAST_UPDATE" AS last_update,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status,
    "CONF_STATUS" AS conf_status,
    "EMBARGO_DATE" AS embargo_date
FROM "ksh-e962bdbf-4809-4904-808f-9df7d45f0c5e"
