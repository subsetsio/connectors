-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "PUR5YP" AS pur5yp,
    CAST("SEXP" AS BIGINT) AS sexp,
    CAST("REGION" AS BIGINT) AS region,
    "REGION_TYPE" AS region_type,
    CAST("STATE" AS BIGINT) AS state,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value
FROM "australian-bureau-of-statistics-c21-g45-lga"
