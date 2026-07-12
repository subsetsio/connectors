-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unit_of_measure",
    "economy_and_households",
    "energy_product",
    CAST("year" AS BIGINT) AS year,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0204000000-106"
