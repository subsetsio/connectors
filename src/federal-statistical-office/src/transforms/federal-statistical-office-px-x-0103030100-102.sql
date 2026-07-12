-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "canton_district_commune",
    "previous_citizenship_selection",
    "sex",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0103030100-102"
