-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gateway_airport",
    CAST("year_2022" AS BIGINT) AS year_2022,
    CAST("year_2023" AS BIGINT) AS year_2023,
    CAST("change_2022_2023" AS DOUBLE) AS change_2022_2023
FROM "u-s-department-of-transportation-hpjf-p2n3"
