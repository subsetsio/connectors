-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "canton",
    "population_type",
    "sex",
    "marital_status",
    "age",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0102010000-102"
