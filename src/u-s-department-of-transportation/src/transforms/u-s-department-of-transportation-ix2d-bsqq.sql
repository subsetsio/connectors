-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "revenues",
    CAST("dollars" AS BIGINT) AS dollars
FROM "u-s-department-of-transportation-ix2d-bsqq"
