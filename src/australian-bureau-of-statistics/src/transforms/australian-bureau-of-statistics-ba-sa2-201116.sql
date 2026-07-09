-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ABS SDMX dataflows may include totals and component categories in the same coded dimensions; filter dimensions deliberately before aggregating observations.
-- caution: The model verifier did not nominate a compact key for this wide cross-tabulation; treat rows as source observations unless a later model pass asserts the full dimension key.
SELECT
    "DATAFLOW" AS dataflow,
    CAST("MEASURE" AS BIGINT) AS measure,
    CAST("SECTOR" AS BIGINT) AS sector,
    "WORK_TYPE" AS work_type,
    "BUILDING_TYPE" AS building_type,
    "REGION_TYPE" AS region_type,
    CAST("REGION" AS BIGINT) AS region,
    "FREQ" AS freq,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MEASURE" AS unit_measure,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "OBS_STATUS" AS obs_status,
    "OBS_COMMENT" AS obs_comment
FROM "australian-bureau-of-statistics-ba-sa2-201116"
