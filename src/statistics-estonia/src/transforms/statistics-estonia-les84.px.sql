-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "head_of_household_type_of_household_child_0_17",
    "indicator",
    "value"
FROM "statistics-estonia-les84.px"
