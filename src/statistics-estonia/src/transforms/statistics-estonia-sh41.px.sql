-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mental_and_physical_health_diseases_consumption_of_medicines",
    "group_of_persons",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-sh41.px"
