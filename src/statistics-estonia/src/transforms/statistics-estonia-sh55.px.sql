-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "body_mass_index_physical_activity_nutrition",
    "health_condition",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-sh55.px"
