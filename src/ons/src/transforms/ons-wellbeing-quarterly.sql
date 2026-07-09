-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This quarterly wellbeing table has duplicate rows under the available raw dimensions; treat rows as source observations and filter estimate, interval, and seasonal-adjustment fields before aggregating.
SELECT
    "value",
    CAST("lcl" AS DOUBLE) AS lcl,
    CAST("ucl" AS DOUBLE) AS ucl,
    "yyyy_qq",
    "time",
    "uk_only",
    "geography",
    "measure_of_wellbeing",
    "measureofwellbeing",
    "wellbeing_estimate",
    "estimate",
    "seasonal_adjustment",
    "seasonaladjustment"
FROM "ons-wellbeing-quarterly"
