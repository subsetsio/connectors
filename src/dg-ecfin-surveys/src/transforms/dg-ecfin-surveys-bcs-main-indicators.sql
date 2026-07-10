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
    "INDICATOR" AS indicator,
    "SEASONAL_ADJUST" AS seasonal_adjust,
    "FREQ" AS freq,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value
FROM "dg-ecfin-surveys-bcs-main-indicators"
