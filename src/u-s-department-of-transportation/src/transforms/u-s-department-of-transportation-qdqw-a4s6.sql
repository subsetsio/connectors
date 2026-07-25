-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "funding",
    "agency",
    "type",
    "outlays",
    "fund",
    CAST("dollars" AS BIGINT) AS dollars
FROM "u-s-department-of-transportation-qdqw-a4s6"
