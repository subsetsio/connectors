-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "mode",
    CAST("date" AS TIMESTAMP) AS date,
    CAST("week_number" AS BIGINT) AS week_number,
    CAST("current_ridership" AS BIGINT) AS current_ridership,
    CAST("baseline" AS BIGINT) AS baseline
FROM "u-s-department-of-transportation-dc74-f8qd"
