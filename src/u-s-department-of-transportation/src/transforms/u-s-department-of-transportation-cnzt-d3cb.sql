-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "station",
    "state",
    CAST("ridership" AS BIGINT) AS ridership,
    CAST("year" AS BIGINT) AS year
FROM "u-s-department-of-transportation-cnzt-d3cb"
