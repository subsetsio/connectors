-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
-- caution: The model verifier did not nominate a compact key for this wide cross-tabulation; treat rows as source observations unless a later model pass asserts the full dimension key.
SELECT
    "DATAFLOW" AS dataflow,
    CAST("SEXP" AS BIGINT) AS sexp,
    "QALLP" AS qallp,
    "OCCP" AS occp,
    "REGION" AS region,
    "REGION_TYPE" AS region_type,
    "STATE" AS state,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value
FROM "australian-bureau-of-statistics-c21-g52-sa2"
