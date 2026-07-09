-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE" AS measure,
    "DATA_ITEM" AS data_item,
    "LOAN_TYPE" AS loan_type,
    "LOAN_PURPOSE" AS loan_purpose,
    "LENDER_TYPE" AS lender_type,
    "BUSINESS_SIZE" AS business_size,
    CAST("TSEST" AS BIGINT) AS tsest,
    "REGION" AS region,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "OBS_STATUS" AS obs_status,
    "OBS_COMMENT" AS obs_comment
FROM "australian-bureau-of-statistics-lend-business"
