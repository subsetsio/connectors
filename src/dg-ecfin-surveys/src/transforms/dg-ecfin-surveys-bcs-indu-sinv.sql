-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ref_area mixes individual countries with supranational aggregates (EU, EA/euro area) and candidate/non-member economies — filter ref_area before aggregating across geographies.
SELECT
    "DATAFLOW" AS dataflow,
    "LAST UPDATE" AS last_update,
    "REF_AREA" AS ref_area,
    "ACTIVITY" AS activity,
    "STRUCTURE_OF_THE_INVESTMENT" AS structure_of_the_investment,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "dg-ecfin-surveys-bcs-indu-sinv"
