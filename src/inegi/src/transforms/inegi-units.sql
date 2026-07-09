-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A unit code can carry more than one description spelling; code alone is not unique.
SELECT
    CAST("code" AS BIGINT) AS code,
    "description"
FROM "inegi-units"
