-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "MM_SEGMENT" AS mm_segment,
    "COUNTERPART_TYPE" AS counterpart_type,
    "TRANSACTION_TYPE" AS transaction_type,
    "UNIT_MEASURE" AS unit_measure,
    "FX_CURRENCY" AS fx_currency,
    "MATURITY" AS maturity,
    "REF_RATE_INDEX" AS ref_rate_index,
    "RATE_TYPE" AS rate_type,
    "COLL_ISSUER_AREA" AS coll_issuer_area,
    "COLL_SEC_TYPE" AS coll_sec_type,
    "COLL_ISIN" AS coll_isin,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value
FROM "norges-bank-money-market"
