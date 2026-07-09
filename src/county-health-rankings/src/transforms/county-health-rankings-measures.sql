-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "release_year",
    "measure_id",
    "measure_name",
    "source_variable",
    "has_raw_value",
    "has_numerator",
    "has_denominator",
    "has_ci_low",
    "has_ci_high"
FROM "county-health-rankings-measures"
