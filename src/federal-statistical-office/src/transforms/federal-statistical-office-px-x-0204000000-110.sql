-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_expenditure",
    "economic_activity",
    "enterprise_size",
    "environmental_domain",
    "results",
    CAST("year" AS BIGINT) AS year,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0204000000-110"
