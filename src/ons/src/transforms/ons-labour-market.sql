-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "mmm_mmm_yyyy",
    "time",
    "uk_only",
    "geography",
    "unit_of_measure",
    "unitofmeasure",
    "economic_activity",
    "economicactivity",
    "age_groups",
    "agegroups",
    "sex",
    "sex_1",
    "seasonal_adjustment",
    "seasonaladjustment"
FROM "ons-labour-market"
