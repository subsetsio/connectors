-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ref_area mixes individual countries with supranational aggregates (EU, EA/euro area) and candidate/non-member economies — filter ref_area before aggregating across geographies.
-- caution: obs_value spans multiple survey indicators reported in different units (see unit_measure: balances vs. percentage shares) — never sum or average obs_value across indicators/units.
SELECT
    "DATAFLOW" AS dataflow,
    "LAST UPDATE" AS last_update,
    "SURVEY" AS survey,
    "REF_AREA" AS ref_area,
    "ACTIVITY" AS activity,
    "INDICATOR" AS indicator,
    "UNIT_MEASURE" AS unit_measure,
    "SEASONAL_ADJUST" AS seasonal_adjust,
    "FREQ" AS freq,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    "OBS_VALUE" AS obs_value
FROM "dg-ecfin-surveys-bcs-cons-sub-5-6"
